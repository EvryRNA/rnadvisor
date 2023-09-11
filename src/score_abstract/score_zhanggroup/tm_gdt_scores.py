"""
Class that returns the scores from the Zhanggroup code to compute :
    - TM-score: a metric to assess the topological similarity of protein structures.
            This is here associated to RNA structures.
    - GDT-TS score (Global Distance Test Total Score): the sum of percent of residues that are
    within the 1, 2, 4 and 8A sphere between a superimposed model and native reference structure,
    divided by 4.

The original code can be found at the following website:
        https://zhanggroup.org/TM-score/
Source for the TM-score:
    Zhang Y, Skolnick J.
    Scoring function for automated assessment of protein structure template quality.
    Proteins. 2004 Dec 1;57(4):702-10. doi: 10.1002/prot.20264.
    Erratum in: Proteins. 2007 Sep 1;68(4):1020. PMID: 15476259.
Source for the GDT-TS score (adapted from the CASP competition):
    Zemla A, Venclovas C, Moult J, Fidelis K. 1999.
    Processing and analysis of CASP3 protein structurepredictions.Proteins3:22–29
"""
import os
import subprocess
import time
from typing import Dict, Optional, Tuple

import numpy as np
from loguru import logger

from src.score_abstract.score_abstract import ScoreAbstract


class TmGdtScores(ScoreAbstract):
    """
    Compute the TM-score and GDT-TS scores using the C++ code from the Zhanggroup.
    It basically runs the C++ code and get the output before parsing the outputs.
    """

    def __init__(self, zhang_bin_path: Optional[str] = None, *args, **kwargs):
        """
        :param zhang_bin_path: path to the binary executable TMScore file
        """
        self.bin_path = (
            zhang_bin_path
            if zhang_bin_path is not None
            else os.path.join("lib", "zhanggroup", "TMscore")
        )
        super(TmGdtScores, self).__init__(*args, **kwargs)

    def _compute(self, pred_path: str, native_path: str) -> Tuple[Dict, Dict]:
        """
        Compute the score for a given prediction and the native .pdb path.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: dictionary with the scores and the given values for the inputs
        """
        all_scores = {}
        # Get the different scores
        time_b = time.time()
        tm_score, gdt_ts, gdt_ts_detailed = self._compute_zhanggroup_scores(
            pred_path, native_path, self.bin_path
        )
        execution_time = time.time() - time_b
        all_scores["TM-SCORE"] = tm_score
        all_scores["GDT-TS"] = gdt_ts
        all_scores = {**all_scores, **gdt_ts_detailed}
        times = {key: execution_time for key in all_scores}
        return all_scores, times

    @staticmethod
    def compute_tm_score(
        pred_path: str,
        native_path: str,
        zhang_bin_path: str = os.path.join("lib", "zhanggroup", "TMscore"),
    ) -> float:
        """
        Compute the TM-score for two RNA structures.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param zhang_bin_path: path to the binary executable TMScore file
        :return: the TM-score given by the Zhanggroup
        """
        tm_score, _, _ = TmGdtScores._compute_zhanggroup_scores(
            pred_path, native_path, zhang_bin_path
        )
        return tm_score

    @staticmethod
    def compute_gdt_ts(
        pred_path: str,
        native_path: str,
        zhang_bin_path: str = os.path.join("lib", "zhanggroup", "TMscore"),
    ) -> float:
        """
        Compute the GDT-TS score for two RNA structures.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param zhang_bin_path: path to the binary executable TMScore file
        :return: the GDT-TS score given by the Zhanggroup
        """
        _, gdt_ts, _ = TmGdtScores._compute_zhanggroup_scores(
            pred_path, native_path, zhang_bin_path
        )
        return gdt_ts

    @staticmethod
    def compute_gdt_ts_detailed(
        pred_path: str,
        native_path: str,
        zhang_bin_path: str = os.path.join("lib", "zhanggroup", "TMscore"),
    ) -> Dict:
        """
        Compute the GDT-TS scores for d<1, d<2, d<4 and d<8 Angstrom for two RNA structures.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param zhang_bin_path: path to the binary executable TMScore file
        :return: a dictionary with as key either '(d<1)', '(d<2)', '(d<4)' or '(d<8)' and the
            associated GDT-TS score
        """
        _, _, gdt_ts_detailed = TmGdtScores._compute_zhanggroup_scores(
            pred_path, native_path, zhang_bin_path
        )
        return gdt_ts_detailed

    @staticmethod
    def _compute_zhanggroup_scores(
        pred_path: str,
        native_path: str,
        zhang_bin_path: str = os.path.join("lib", "zhanggroup", "TMscore"),
    ) -> Tuple[float, float, Dict]:
        """
        Compute different scores from the Zhanggroup TMScore.cpp file
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param zhang_bin_path: path to the binary executable TMScore file
        :return: the TM score, GDT-TS score and a dictionary with the score for
            d<1, d<2, d<4 and d<8 for the GDT-TS score
        """
        # Get the shell command that will be executed
        command = f"{zhang_bin_path} {pred_path} {native_path} | grep -E '^TM-score|GDT-TS'"
        distances = [1, 2, 4, 8]
        try:
            output = subprocess.check_output(command, shell=True)
            scores = str(output.decode()).split("\n")
            # Convert the output of the shell command to scores
            tm_score, gdt_ts = float(scores[0].split()[2]), float(scores[1].split()[1])
            # Get the d<1, d<2, d<4 and d<8 values for the GDT-TS score
            gdt_ts_detailed = {
                f"GDT-TS@{distances[index]}": float(value.split("=")[1])
                for index, value in enumerate(scores[1].split("%")[1:])
            }
            return tm_score, gdt_ts, gdt_ts_detailed
        except subprocess.CalledProcessError:
            logger.debug(f"PATH TO TMscore binary not found : {zhang_bin_path}")
            return np.nan, np.nan, {f"GDT-TS@{distance}": np.nan for distance in distances}
