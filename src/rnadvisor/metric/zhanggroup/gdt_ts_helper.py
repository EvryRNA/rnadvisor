"""
Class that returns the scores from the Zhanggroup code to compute :
    GDT-TS score (Global Distance Test Total Score): the sum of percent of residues that are
    within the 1, 2, 4 and 8A sphere between a superimposed model and native reference structure,
    divided by 4.

The original code can be found at the following website:
        https://zhanggroup.org/TM-score/
Source for the GDT-TS score (adapted from the CASP competition):
    Zemla A, Venclovas C, Moult J, Fidelis K. 1999.
    Processing and analysis of CASP3 protein structure predictions. Proteins3:22–29
"""

import os
import subprocess
import time
from typing import Dict, Optional, Tuple

import numpy as np
from loguru import logger

from rnadvisor.predict_abstract import PredictAbstract
from rnadvisor.cli_runner import build_predict_cli




class GdtTsHelper(PredictAbstract):
    """
    Compute the GDT-TS scores using the C++ code from the Zhanggroup.
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
        super(GdtTsHelper, self).__init__(name="GDT-TS",*args, **kwargs)

    def predict_single_file(
        self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the score for a given prediction and the native .pdb path.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: dictionary with the scores and the given values for the inputs
        """
        all_scores = {}
        # Get the different scores
        time_b = time.time()
        gdt_ts, gdt_ts_detailed = self._compute_zhanggroup_scores(
            pred_path, native_path, self.bin_path
        )
        execution_time = time.time() - time_b
        all_scores["GDT-TS"] = gdt_ts
        all_scores = {**all_scores, **gdt_ts_detailed}
        times = {key: execution_time for key in all_scores}
        return all_scores, times

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
        gdt_ts, _ = GdtTsHelper._compute_zhanggroup_scores(pred_path, native_path, zhang_bin_path)
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
        _, gdt_ts_detailed = GdtTsHelper._compute_zhanggroup_scores(
            pred_path, native_path, zhang_bin_path
        )
        return gdt_ts_detailed

    @staticmethod
    def _compute_zhanggroup_scores(
        pred_path: str,
        native_path: str,
        zhang_bin_path: str = os.path.join("lib", "zhanggroup", "TMscore"),
    ) -> Tuple[float, Dict]:
        """
        Compute different scores from the Zhanggroup TMScore.cpp file
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param zhang_bin_path: path to the binary executable TMScore file
        :return: GDT-TS score and a dictionary with the score for
            d<1, d<2, d<4 and d<8 for the GDT-TS score
        """
        # Get the shell command that will be executed
        command = f"{zhang_bin_path} {pred_path} {native_path} | grep -E 'GDT-TS'"
        distances = [1, 2, 4, 8]
        try:
            output = subprocess.check_output(command, shell=True)
            scores = str(output.decode()).split("\n")
            # Convert the output of the shell command to scores
            gdt_ts = float(scores[0].split()[1])
            # Get the d<1, d<2, d<4 and d<8 values for the GDT-TS score
            gdt_ts_detailed = {
                f"GDT-TS@{distances[index]}": float(value.split("=")[1])
                for index, value in enumerate(scores[0].split("%")[1:])
            }
            return gdt_ts, gdt_ts_detailed
        except subprocess.CalledProcessError:
            logger.debug(f"PATH TO TMscore binary not found : {zhang_bin_path}")
            return np.nan, {f"GDT-TS@{distance}": np.nan for distance in distances}

main = build_predict_cli(GdtTsHelper)

if __name__ == "__main__":
    main()
