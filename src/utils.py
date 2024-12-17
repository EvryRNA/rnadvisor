"""Useful functions."""

import time
from typing import Any, Dict, Tuple

import yaml  # type: ignore
from loguru import logger
from Bio.PDB import (
    PDBParser,
    MMCIFIO,
    MMCIFParser,
    PDBIO,
    FastMMCIFParser,
    Atom,
    Model,
    Chain,
    Residue,
    Structure,
    PDBParser,
)


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


def convert_cif_to_pdb(in_cif: str, out_pdb: str):
    """
    Convert a .cif file to a .pdb file, handling multiple chains and chain ID limits.
    :param in_cif: Path to the input .cif file
    :param out_pdb: Path to save the output .pdb file
    """
    try:
        parser = MMCIFParser(QUIET=True)
        structure = parser.get_structure("my_structure", in_cif)
        used_chain_ids = set()
        remap_chain_ids = {}
        # Handle chain IDs
        for model in structure:
            for chain in model:
                original_id = chain.id
                if len(original_id) > 1 or original_id in used_chain_ids:
                    # Generate a new chain ID
                    for new_id in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                        if new_id not in used_chain_ids:
                            remap_chain_ids[original_id] = new_id
                            chain.id = new_id
                            used_chain_ids.add(new_id)
                            break
                    else:
                        raise ValueError("Too many chains to fit in PDB format!")
                else:
                    used_chain_ids.add(original_id)
        io = PDBIO()
        io.set_structure(structure)
        io.save(out_pdb)
    except Exception as e:
        print(f"Error during conversion: {e}")
