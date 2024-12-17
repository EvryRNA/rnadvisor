import os
import subprocess
from typing import Tuple, Dict, Optional

from src.utils import time_it
from src.score_abstract.score_abstract import ScoreAbstract


class TMScoreUS(ScoreAbstract):
    """
    Compute the TM-Score score using the C++ code from the Zhanggroup US-Align.
                    (https://zhanggroup.org/US-align/)
        Chengxin Zhang, Morgan Shine, Anna Marie Pyle, Yang Zhang.
        US-align: Universal Structure Alignment of Proteins,
        Nucleic Acids and Macromolecular Complexes.
        Nature Methods, 19: 1109-1115 (2022)
    It basically runs the C++ code and get the output before parsing the outputs.
    """

    def __init__(self, zhang_bin_path_us: Optional[str] = None, *args, **kwargs):
        """
        :param zhang_bin_path_us: path to the binary executable US-Align file
        """
        self.bin_path = (
            zhang_bin_path_us
            if zhang_bin_path_us is not None
            else os.path.join("lib", "zhanggroup", "USalign")
        )
        super(TMScoreUS, self).__init__(*args, **kwargs)

    @time_it
    def _compute(self, pred_path: str, native_path: str, *args, **kwargs) -> Tuple[Dict, Dict]:
        """
        Compute the TM-score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the TM-score
        """
        tm_score = self.compute_tm_score(pred_path, native_path, self.bin_path)
        return {"TM-score": tm_score}  # type: ignore

    @staticmethod
    def compute_tm_score(
        pred_path: str,
        native_path: str,
        zhang_bin_path_us: Optional[str] = os.path.join("lib", "zhanggroup", "USalign"),
    ) -> float:
        """
        Compute the TM-score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the TM-score for the prediction.
        """
        command = f"{zhang_bin_path_us} -mol RNA {pred_path} {native_path} | grep -E 'TM-score'"
        output = subprocess.check_output(command, shell=True)
        scores = str(output.decode()).split("\n")
        tm_score = float(scores[1].split()[1])
        return tm_score
