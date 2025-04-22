import shutil
import subprocess  # nosec
import sys
import uuid
from pathlib import Path
from typing import Dict

import yaml  # type: ignore
from loguru import logger


def is_command_available(cmd_list):
    try:
        subprocess.run(
            cmd_list,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,  # nosec
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_docker_compose():
    if is_command_available(["docker", "compose", "version"]):
        return ["docker", "compose"]
    elif shutil.which("docker-compose") and is_command_available(
        ["docker-compose", "version"]
    ):
        return ["docker-compose"]
    else:
        logger.warning(
            "Neither 'docker compose' nor 'docker-compose' is installed or working properly."
        )
        sys.exit(1)


def delete_docker_network(name: str):
    """
    Delete the docker network with the given name.
    :param name: name of the network to delete
    """
    subprocess.run(["docker", "network", "rm", name], check=False)  # nosec


def ensure_docker_network(name="rnadvisor_shared_net"):
    result = subprocess.run(  # nosec
        ["docker", "network", "ls", "--format", "{{.Name}}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("❌ Failed to list Docker networks. Is Docker running?")
    if name not in result.stdout.splitlines():
        subprocess.run(["docker", "network", "create", name], check=True)  # nosec


def run_services_docker(services: Dict, volumes: Dict, verbose: int, dc_tmp_path: str):
    """
    Launch docker compose up for the services defined in the compose file.
    Skips any services whose images cannot be found.
    """
    network_name = f"rnadvisor_net_{uuid.uuid4().hex[:6]}"
    compose_cmd = check_docker_compose()
    try:
        ensure_docker_network(network_name)
        compose_dict = get_compose_dict(services, volumes, network_name, verbose)
        if not compose_dict["services"]:
            logger.warning("❌ No valid services to run.")
            return
        with Path(dc_tmp_path).open("w") as f:
            yaml.dump(compose_dict, f, sort_keys=False)
        subprocess.run(compose_cmd + ["-f", dc_tmp_path, "up"])  # nosec
    finally:
        # Clean all the files
        delete_docker_network(network_name)
        Path(dc_tmp_path).unlink(missing_ok=True)
        subprocess.run(compose_cmd + ["-f", dc_tmp_path, "down"], check=False)  # nosec


def get_compose_dict(
    services: Dict, volumes: Dict, network_name: str, verbose: int
) -> Dict:
    """
    Return the docker compose dictionnary to run the different services
    :param services: the name of the metrics/scoring functions to run
    :param network_name: the name of the docker network to use
    :param verbose: the verbosity level
    :param volumes: the different volumes to mount
    :return: a docker-compose config with the services to run
    """
    compose_dict = {
        "services": {},
        "networks": {"rnadvisor_net": {"name": network_name, "external": True}},
    }
    for service, config in services.items():
        image = f"sayby77/rnadvisor-{service}-slim"
        args = config.get("args", {})
        command = []
        for key, val in args.items():
            if val != "":
                command.append(key)
                command.append(str(val))
        if verbose <= 1:
            command.append("--quiet")

        volume_mounts = [f"{host}:{container}" for host, container in volumes.items()]

        compose_dict["services"][f"rnadvisor-{service}"] = {  # type: ignore
            "image": image,
            "command": command,
            "stdin_open": True,
            "tty": True,
            "restart": "no",
            "platform": "linux/amd64",
            "volumes": volume_mounts,
            "networks": ["rnadvisor_net"],
        }
    return compose_dict
