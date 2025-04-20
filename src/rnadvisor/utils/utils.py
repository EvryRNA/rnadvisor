import sys
import time
from typing import Any, List, Tuple

from loguru import logger
from tqdm import tqdm

try:
    from Bio.PDB import PDBIO, MMCIFParser  # type: ignore
    from rna_tools.rna_tools_lib import RNAStructure, add_header  # type: ignore
except ImportError:
    RNAStructure = None
    add_header = None

from rnadvisor.enums.list_dockers import ALL, ALL_METRICS, ALL_SF, SERVICES


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


def read_txt_file(in_path: str) -> List[str]:
    """
    Read a txt file and return a list of lines
    :param in_path: path to a .txt file
    :return: list of the lines
    """
    with open(in_path, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def write_to_txt_file(out_path: str, lines: List[str]) -> None:
    """
    Write a list of lines to a txt file
    :param out_path: path to a .txt file
    :param lines: list of the lines
    """
    with open(out_path, "w") as f:
        for line in lines:
            f.write(line + "\n")


class TqdmCompatibleHandler:
    def write(self, message):
        tqdm.write(message.strip())

    def flush(self):
        pass


def init_logger(verbosity: int = 1):
    """
    Initialise the logger with verbosity levels:
    0 = No logging
    1 = INFO and above (excluding DEBUG)
    2 = Full logging including DEBUG
    """
    logger.remove()
    if verbosity == 0:
        return None
    level = "DEBUG" if verbosity >= 2 else "INFO"
    filter_fn = None if verbosity == 2 else lambda r: r["level"].no >= 20

    handler = sys.stderr if verbosity == 2 else TqdmCompatibleHandler()

    logger.add(  # type: ignore
        handler,
        level=level,
        filter=filter_fn,
        colorize=True,
        backtrace=True,
        diagnose=True,
        enqueue=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level:<8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
    )


def check_scores(scores: List[str]) -> List[str]:
    """
    Check the given metrics/scoring functions to use.
    :param scores: list of metrics/scoring functions to use, or keywords like "ALL", "METRICS", "SF"
    :return: list of valid metrics/scoring functions that can be used
    """
    expanded_scores = []
    for score in scores:
        score_lower = (
            score.lower().replace("escore", "barnaba").replace("ermsd", "barnaba")
        )
        if score_lower == "all":
            expanded_scores.extend(ALL)
        elif score_lower == "metrics":
            expanded_scores.extend(ALL_METRICS)
        elif score_lower == "sf":
            expanded_scores.extend(ALL_SF)
        else:
            expanded_scores.append(score_lower)
    # Make the list unique and filter valid scores
    unique_scores = list(set(expanded_scores))
    return [score for score in unique_scores if score in SERVICES]


def save_pdb_rna_tools(structure: Any, out_path: str):
    """
    Code from https://github.com/mmagnus/rna-tools/blob/master/rna_tools/rna_pdb_tools.py
    :param structure: RNAStructure object
    :param out_path: path where to save the structure
    """
    output = ""
    output += add_header("") + "\n"
    output += structure.get_text() + "\n"
    with open(out_path, "w") as fio:
        fio.write(output)


def clean_structure_rna_tools(in_path: str, out_path: str):
    """
    Clean the structure and make it ready for evaluation using RNA-tools.
    Code from https://github.com/mmagnus/rna-tools/blob/master/rna_tools/rna_pdb_tools.py
    :param in_path: path to a .pdb file
    :param out_path: path where to save the clean structure.
    """
    structure = RNAStructure(in_path)
    structure.get_rnapuzzle_ready(verbose=False)
    save_pdb_rna_tools(structure, out_path)


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
