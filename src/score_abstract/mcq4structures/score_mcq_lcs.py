"""
Class that runs the LCS-TA code
The original github code is the following:
    https://github.com/tzok/mcq4structures
The original paper is :
Wiedemann, J., Zok, T., Milostan, M., & Szachniuk, M. (2017).
LCS-TA to identify similar fragments in RNA 3D structures.
BMC Bioinformatics, 18(1), 456. https://doi.org/10.1186/s12859-017-1867-6
"""

import os
import subprocess
from typing import Dict, Optional, Tuple
import time

import numpy as np

from src.score_abstract.score_abstract import ScoreAbstract


class ScoreMCQLCS(ScoreAbstract):
    def __init__(self, mcq_bin_path: Optional[str] = None, *args, **kwargs):
        super(ScoreMCQLCS, self).__init__(*args, **kwargs)
        self.mcq_bin_path = mcq_bin_path

    @staticmethod
    def compute_mcq_lcs(
        pred_path: str,
        native_path: str,
        mcq_bin_path: Optional[str] = None,
        mcq_threshold: float = 25,
    ) -> Tuple[float, float]:
        """
        Compute the LCS-TA metric (using the mcq-lcs of the mcq4structures code)
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param mcq_bin_path: the binary path to the mcq-lcs file
        :param mcq_threshold: threshold used for the computation of the longest sequence
        :return: the coverage and number of residues
        """
        mcq_bin_path = (
            mcq_bin_path
            if mcq_bin_path is not None
            else os.path.join("lib", "mcq4structures", "mcq-cli", "mcq-local")
        )
        mcq_bin_path = mcq_bin_path.replace("mcq-local", "mcq-lcs")
        # Get the shell command that will be executed
        command = (
            f"{mcq_bin_path} -t {native_path} {pred_path} -v {mcq_threshold} "
            f"> tmp/mcq_out.txt 2> /dev/null"
        )
        os.system(command)
        command_cov = "cat tmp/mcq_out.txt | awk '/Coverage/ {print $2}'"
        command_nb = "cat tmp/mcq_out.txt | awk '/Number of residues/ {print $4}'"
        output_cov = subprocess.check_output(command_cov, shell=True, stderr=subprocess.DEVNULL)
        output_nb = subprocess.check_output(command_nb, shell=True, stderr=subprocess.DEVNULL)
        command_del = "rm tmp/mcq_out.txt"
        os.system(command_del)
        try:
            coverage = str(output_cov.decode()).replace("\n", "")
            lcs_coverage = float(coverage[:-1])  # Remove the "%"
            nb_residue = float(str(output_nb.decode()).replace("\n", ""))
        except ValueError:
            lcs_coverage, nb_residue = np.nan, np.nan
        return lcs_coverage, nb_residue  # type: ignore

    def _compute(self, pred_path: str, native_path: str) -> Tuple[Dict, Dict]:
        """
        Compute the LCS-TA metrics for a given prediction and the native .pdb path.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: dictionary with the MCQ score for the given inputs
        """
        time_b = time.time()
        lcs_coverage, nb_residue = self.compute_mcq_lcs(pred_path, native_path, self.mcq_bin_path)
        time_complete = time.time() - time_b
        scores = {"LCS-TA-COVERAGE": lcs_coverage, "LCS-TA-RESIDUES": nb_residue}
        out_time = {key: time_complete for key in scores}
        return scores, out_time
