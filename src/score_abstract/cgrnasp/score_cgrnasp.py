"""
Class that implements the cgRNASP score.

Original code from:
https://github.com/Tan-group/cgRNASP/tree/main/cgRNASP

I used a fork to remove training data, and modify the CLI:

Original paper:

Tan YL, Wang X, Yu S, Zhang B, & Tan ZJ. 2023.
cgRNASP: coarse-grained statistical potentials with residue separation
for RNA structure evaluation.
NAR Genom Bioinform. 5(1): lqad016.
"""

from typing import Optional, Tuple, Dict
from src.score_abstract.score_abstract import ScoreAbstract
from src.utils import fn_time
import os
import subprocess


class ScoreCGRNASP(ScoreAbstract):
    """
    Class that implements the cgRNASP code.
    """

    def __init__(self, cgrnasp_bin_path: Optional[str] = None, *args, **kwargs):
        super(ScoreCGRNASP, self).__init__(*args, **kwargs)
        self.cgrnasp_bin_path = (
            cgrnasp_bin_path
            if cgrnasp_bin_path is not None
            else os.path.join("lib", "cgRNASP", "bin")
        )

    @staticmethod
    def compute_cgrnasp(pred_path: str, cgrnasp_bin_path: Optional[str] = None) -> float:
        """
        Compute the cgRNASP score.
        :param pred_path: the path to the .pdb file of a prediction.
        :param cgrnasp_bin_path: the binary path to the cgRNASP file
        :return: the cgRNASP score
        """
        cgrnasp_bin_path = (
            cgrnasp_bin_path
            if cgrnasp_bin_path is not None
            else os.path.join("lib", "cgRNASP", "bin")
        )
        bin_path = os.path.join(cgrnasp_bin_path, "cgRNASP_bin")
        command = f"{bin_path} {pred_path}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        cgrnasp = output.decode().replace("\n", "").split()[-1]
        return round(float(cgrnasp), 3)

    @staticmethod
    def compute_cgrnasp_c(pred_path: str, cgrnasp_bin_path: Optional[str] = None) -> float:
        """
        Compute the cgRNASP-C score.
        :param pred_path: the path to the .pdb file of a prediction.
        :param cgrnasp_bin_path: the binary path to the cgRNASP file
        :return: the cgRNASP-C score
        """
        cgrnasp_bin_path = (
            cgrnasp_bin_path
            if cgrnasp_bin_path is not None
            else os.path.join("lib", "cgRNASP", "bin")
        )
        bin_path = os.path.join(cgrnasp_bin_path, "cgRNASP-C_bin")
        command = f"{bin_path} {pred_path}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        cgrnasp_c = output.decode().replace("\n", "").split()[-1]
        return round(float(cgrnasp_c), 3)

    @staticmethod
    def compute_cgrnasp_pc(pred_path: str, cgrnasp_bin_path: Optional[str] = None) -> float:
        """
        Compute the cgRNASP-PC score.
        :param pred_path: the path to the .pdb file of a prediction.
        :param cgrnasp_bin_path: the binary path to the cgRNASP file
        :return: the cgRNASP-PC score
        """
        cgrnasp_bin_path = (
            cgrnasp_bin_path
            if cgrnasp_bin_path is not None
            else os.path.join("lib", "cgRNASP", "bin")
        )
        bin_path = os.path.join(cgrnasp_bin_path, "cgRNASP-PC_bin")
        command = f"{bin_path} {pred_path}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        cgrnasp_pc = output.decode().replace("\n", "").split()[-1]
        return round(float(cgrnasp_pc), 3)

    def _compute(self, pred_path: str, native_path: str, *args, **kwargs) -> Tuple[Dict, Dict]:
        """
        Compute the cgRNASP, cgRNASP-C and cgRNASP-PC scores.
        """
        cgrnasp, cgrnasp_time = fn_time(self.compute_cgrnasp, pred_path, self.cgrnasp_bin_path)
        cgrnasp_c, cgrnasp_c_time = fn_time(
            self.compute_cgrnasp_c, pred_path, self.cgrnasp_bin_path
        )
        cgrnasp_pc, cgrnasp_pc_time = fn_time(
            self.compute_cgrnasp_pc, pred_path, self.cgrnasp_bin_path
        )
        scores = {"cgRNASP": cgrnasp, "cgRNASP-C": cgrnasp_c, "cgRNASP-PC": cgrnasp_pc}
        times = {
            "cgRNASP": cgrnasp_time,
            "cgRNASP-C": cgrnasp_c_time,
            "cgRNASP-PC": cgrnasp_pc_time,
        }
        return scores, times
