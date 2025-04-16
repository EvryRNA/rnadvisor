"""
Class that implements the RNA-BRiQ code.

Original code from:
https://github.com/Jian-Zhan/RNA-BRiQ

Wrapper for this code was done with the help of Thomasz Zok who did the C++ code for the energy.

Original paper:
Xiong P, Wu R, Zhan J, Zhou Y.
Pairing a high-resolution statistical potential with a nucleobase-centric sampling algorithm
for improving RNA model refinement.
Nat Commun.
2021 May 13;12(1):2777. doi: 10.1038/s41467-021-23100-4.
PMID: 33986288; PMCID: PMC8119458.
"""
import os
import subprocess
from typing import Optional, List, Tuple, Dict

from loguru import logger
from tqdm import tqdm
from rnadvisor.utils.utils import time_it, read_txt_file, write_to_txt_file
from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract

SS_COMMAND = "RNA-BRiQ/build/bin/BRiQ_AssignSS $INPUT_PATH $OUTPUT_PATH"
ENERGY_COMMAND = "RNA-BRiQ/build/bin/BRiQ_Energy $INPUT_PATH"

class RNABRiQHelper(PredictAbstract):
    """
    Class that implements the RNA-BRiQ scoring function
    """

    def __init__(self, *args, **kwargs):
        super(RNABRiQHelper, self).__init__(name="rna_briq",*args, **kwargs)
        self.tmp_dir = os.path.join("tmp", "rna_briq")
        os.makedirs(self.tmp_dir, exist_ok=True)


    def prepare_data(self, native_path: Optional[str], pred_paths: List[str], *args, **kwargs):
        """
        Prepare the data for the scoring function.
        It will assign the secondary structure to the input files.
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_paths: list of paths to RNA `.pdb` files.
        """
        logger.debug("Preparing data for RNA-BRiQ scoring function. Assign 2D structure.")
        for pred_path in tqdm(pred_paths):
            out_path = os.path.join(self.tmp_dir, os.path.basename(pred_path))
            command = SS_COMMAND.replace("$INPUT_PATH", pred_path).replace("$OUTPUT_PATH", out_path)
            if not os.path.exists(out_path):
                os.system(command)
            content = read_txt_file(out_path)
            new_content = [f"pdb {pred_path}"] + content
            write_to_txt_file(out_path, new_content)

    def predict_rna_briq(self, pred_path: str):
        """Do the prediction of the RNA-BRiQ scoring function."""
        in_path = os.path.join(self.tmp_dir, os.path.basename(pred_path))
        command = ENERGY_COMMAND.replace("$INPUT_PATH", in_path)
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        # Get the last line of the output
        lines = str(output.decode()).split("\n")
        score = float(lines[-2].split(" ")[-1])
        return score

    @time_it
    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        score = self.predict_rna_briq(pred_path)
        return {"RNA-BRiQ": score}  # type: ignore

main = build_predict_cli(RNABRiQHelper)

if __name__ == "__main__":
    main()
