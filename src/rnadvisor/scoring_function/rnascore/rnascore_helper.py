"""
Class that runs the 3dRNAscore
The original github code is the following:
    http://biophy.hust.edu.cn/new/resources/3dRNAscore
The original paper is:
Wang J, Zhao Y, Zhu C, Xiao Y.
3dRNAscore: a distance and torsion angle dependent evaluation function of 3D RNA structures.
Nucleic Acids Res.
2015 May 26;43(10):e63.
doi: 10.1093/nar/gkv141.
Epub 2015 Feb 24. PMID: 25712091; PMCID: PMC4446410.
"""
import os
from typing import Optional, Dict, Tuple

import numpy as np
import subprocess


from rnadvisor.utils.utils import time_it

from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract


class RNAScore(PredictAbstract):
    def __init__(self, bin_path: str = os.path.join("lib", "3drnascore", "3dRNAscore", "bin", "3dRNAscore"), *args, **kwargs):
        super().__init__(name="3drnascore", *args, **kwargs)
        self.bin_path = bin_path
        os.environ["RNAscore"] = os.path.abspath(os.path.dirname(os.path.dirname(bin_path)))

    @time_it
    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the 3dRNAscore score for a given structure.
        :param pred_path: the path to the .pdb file of a prediction.
        :return: 3dRNAscore
        """
        score = self.compute_3drnascore(pred_path)
        return {self.name: score}  # type: ignore

    def compute_3drnascore(self, rna_path: str) -> float:
        command = f"{self.bin_path} -s {rna_path}"
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
            score = output.decode().replace("\n", "")
            score = round(float(score), 3)
        except subprocess.CalledProcessError:
            score = np.nan
        return score

main = build_predict_cli(RNAScore)

if __name__ == "__main__":
    main()

