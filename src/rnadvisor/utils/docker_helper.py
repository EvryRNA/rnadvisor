from typing import List, Dict
from loguru import logger
import subprocess
from concurrent.futures import ThreadPoolExecutor
import docker
from docker.errors import NotFound
import threading
import sys


def build_docker(scores: List[str]):
    """Build the docker images for the different metrics/scoring functions only if not already available locally."""
    def pull_image(score):
        image_name = f"sayby77/rnadvisor-{score}-slim"
        result = subprocess.run(["docker", "image", "inspect", image_name],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            logger.info(f"Docker image {image_name} already available locally. Skipping pull.")
            return
        logger.info(f"Pulling docker image {image_name}...")
        subprocess.run(["docker", "pull", image_name], check=True)
        logger.info(f"Docker image {image_name} pulled successfully.")

    with ThreadPoolExecutor() as executor:
        executor.map(pull_image, scores)

def run_services_docker(services: Dict, volumes: Dict, verbose: int) -> List:
    """
    Return the different docker images to run
    :param services: a dictionary of services with the different arguments
    :param volumes: mapping between the local and container paths
    :param verbose: verbosity level
    """
    client = docker.from_env()
    processes = []
    for service, config in services.items():
        image = f"sayby77/rnadvisor-{service}-slim"
        args = config.get("args", {})
        command = []
        for key, val in args.items():
            if val != "":
                command.append(key)
                command.append(val)
        if verbose <= 1:
            command+=["--quiet"]
        volume_mounts = {
            host_path: {"bind": container_path, "mode": "rw"}
            for host_path, container_path in volumes.items()
        }
        container = client.containers.run(
            image=image,
            command=command,
            volumes=volume_mounts,
            detach=True,
            remove=True,
            stdin_open=True,
            stream=True,
        )
        logger.info(f"[{service}] Started container: {container.short_id}")
        processes.append((service, container))
    return processes

def wait_services(processes: List):
    """
    Run and wait for the different docker images to finish
    :param processes: a list of processes to wait for
    """
    threads = []
    for service, container in processes:
        t = threading.Thread(target=handle_container, args=(service, container))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def handle_container(service, container):
    """
    Handle the container output and wait for it to finish
    :param service: name of the image
    :param container: container object that is running
    """
    try:
        logger.info(f"📦 Streaming logs for {service}...")

        output = container.attach(stdout=True, stderr=True, stream=True, logs=True)

        for line in output:
            decoded = line.decode(errors="replace")
            if "\r" in decoded:
                sys.stdout.write(f"[{service}] {decoded}")
                sys.stdout.flush()
            else:
                logger.info(f"[{service}] {decoded.rstrip()}")
        result = container.wait()
        ret_code = result.get("StatusCode", -1)
    except NotFound:
        logger.warning(f"[{service}] Container not found (already removed?)")
        ret_code = -1
    except Exception as e:
        logger.error(f"[{service}] Unexpected error: {e}")
        ret_code = -1

    if ret_code == 0:
        logger.info(f"✅ {service} completed successfully ✅")
    else:
        logger.error(f"❌ {service} exited with error code {ret_code} ❌")

def get_cmd_docker(service: str, volumes: Dict) -> List:
    """
    Return the docker command to run the given container
    :param service: name of the metric/scoring function
    :param volumes: mapping between the local and container paths
    :return: command to run the container
    """
    cmd = ["docker", "run", "--rm"]
    for key, val in volumes.items():
        if val is not None:
            cmd += ["-v", f"{key}:{val}"]
    service_name = f"sayby77/rnadvisor-{service}-slim"
    cmd+= [service_name]
    return cmd
