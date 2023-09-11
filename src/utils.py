"""Useful functions."""
import time
from typing import Any, Dict, Tuple

import yaml  # type: ignore
from loguru import logger


def read_yaml_to_dict(path: str) -> Dict:
    """
    Read a .yaml file and convert it to dictionary
    :param path: path to a .yaml file
    :return: a dictionary
    """
    with open(path, "r") as f:
        try:
            content = yaml.safe_load(f)
            return content
        except yaml.YAMLError as e:
            logger.debug(f"ERROR READING YAML FILE : {path} : {e}")
    return {}


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        time_result = {list(result.keys())[0]: execution_time}
        return result, time_result

    return wrapper


def fn_time(func, *args, **kwargs) -> Tuple[Any, float]:
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time
