import shutil
import subprocess  # nosec
import sys
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


def run_services_docker(services: Dict, volumes: Dict, verbose: int, dc_tmp_path: str):
    """
    Launch docker compose up for the services defined in the compose file.
    Skips any services whose images cannot be found.
    """
    compose_dict = {"version": "3.9", "services": {}}

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
        }

    if not compose_dict["services"]:
        logger.warning("❌ No valid services to run.")
        return

    compose_cmd = check_docker_compose()
    with Path(dc_tmp_path).open("w") as f:
        yaml.dump(compose_dict, f, sort_keys=False)
    subprocess.run(compose_cmd + ["-f", dc_tmp_path, "up"])  # nosec
