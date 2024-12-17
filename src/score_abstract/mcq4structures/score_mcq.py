"""
Class that runs the MCQ4Structures code to get the MCQ Score.
The original github code is the following:
    https://github.com/tzok/mcq4structures
The original paper is :
Zok, T., Popenda, M., & Szachniuk, M. (2014).
MCQ4Structures to compute similarity of molecule structures.
Central European Journal of Operations Research, 22(3), 457–473.
https://doi.org/10.1007/s10100-013-0296-5
"""

import os
import subprocess
from typing import Dict, Optional, Tuple

import numpy as np

from src.score_abstract.score_abstract import ScoreAbstract
from src.utils import time_it


class ScoreMCQ(ScoreAbstract):
    def __init__(self, mcq_bin_path: Optional[str] = None, *args, **kwargs):
        super(ScoreMCQ, self).__init__(*args, **kwargs)
        self.mcq_bin_path = mcq_bin_path

    @staticmethod
    def compute_mcq(
        pred_path: str, native_path: str, mcq_bin_path: Optional[str] = None, mcq_mode: int = 2
    ) -> float:
        """
        Compute the MCQ Score (using the mcq-local of the mcq4structures code)
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param mcq_bin_path: the binary path to the mcq-local file
        :param mcq_mode: mode to use with the MCQ: (0: relaxed, 1: compare without violations
            and 2: compare everything regardless of the violations)
        :return: the MCQ Score of the pred and native files
        """
        mcq_bin_path = (
            mcq_bin_path
            if mcq_bin_path is not None
            else os.path.join("lib", "mcq4structures", "mcq-cli", "mcq-local")
        )
        # Get the shell command that will be executed
        command = (
            f"{mcq_bin_path} -r {mcq_mode} -t {native_path} -d tmp {pred_path}"
            + " | awk '{print $NF}' 2> /dev/null"
        )
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        try:
            mcq_score = float(str(output.decode()).replace("\n", ""))
        except ValueError:
            mcq_score = np.nan
        return mcq_score

    @time_it
    def _compute(
        self, pred_path: str, native_path: str, mcq_mode: int, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the MCQ score for a given prediction and the native .pdb path.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param mcq_mode: mode to use with the MCQ: (0: relaxed, 1: compare without violations
            and 2: compare everythinig regardless of the violations)
        :return: dictionary with the MCQ score for the given inputs
        """
        mcq_score = self.compute_mcq(pred_path, native_path, self.mcq_bin_path, mcq_mode)
        return {"MCQ": mcq_score}  # type: ignore
