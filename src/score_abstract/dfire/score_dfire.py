"""
Implementation of the Knowledge-based statistical energy based on DFIRE reference state.

Original code:
https://github.com/tcgriffith/dfire_rna

Original paper:
T. Zhang, G. Hu, Y. Yang, J. Wang, and Y. Zhou,
“All-atom knowledge-based potential for RNA structure discrimination based on the
distance-scaled finite ideal-gas reference state.”,
J. Computational Biology, in press (2019).
"""

import os
import subprocess
from typing import Dict, Optional, Tuple

from src.score_abstract.score_abstract import ScoreAbstract
from src.utils import time_it


class ScoreDfire(ScoreAbstract):
    def __init__(self, dfire_bin_path: Optional[str] = None, *args, **kwargs):
        super(ScoreDfire, self).__init__(*args, **kwargs)
        self.dfire_bin_path = dfire_bin_path

    @time_it
    def _compute(self, pred_path: str, native_path: str, *args, **kwargs) -> Tuple[Dict, Dict]:
        """
        Compute the dfire score
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path:
        :return: dfire score
        """
        dfire = self.compute_dfire(pred_path, self.dfire_bin_path)
        return {"DFIRE": dfire}  # type: ignore

    @staticmethod
    def compute_dfire(pred_path: str, dfire_bin_path: Optional[str] = None) -> float:
        """
        Compute the dfire from the binary file.
        :param pred_path: the path to the .pdb file of a prediction.
        :param dfire_bin_path: the binary path to the DFIRE_RNA file
        :return: the Dfire score
        """
        dfire_bin_path = (
            dfire_bin_path
            if dfire_bin_path is not None
            else os.path.join("lib", "dfire", "bin", "DFIRE_RNA")
        )
        command = f"{dfire_bin_path} {pred_path}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        dfire = output.decode().replace("\n", "").split()[-1]
        dfire = round(float(dfire), 3)  # type: ignore
        return dfire  # type: ignore
