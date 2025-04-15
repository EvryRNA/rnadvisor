"""
File that implements the baRNAba scores.
Original code from:
https://github.com/srnas/barnaba
I created a fork with some changes:
https://github.com/clementbernardd/barnaba/tree/scoring-version
Original paper:
Bottaro, Sandro, Francesco Di Palma, and Giovanni Bussi.
"The role of nucleobase interactions in RNA structure and dynamics."
Nucleic acids research 42.21 (2014): 13306-13314.
"""

from typing import Dict, Tuple, Optional

import lib.barnaba.barnaba as bb
import numpy as np
from lib.barnaba.barnaba import escore

from rnadvisor.predict_abstract import PredictAbstract

from rnadvisor.utils.utils import fn_time

from rnadvisor.cli_runner import build_predict_cli


class BarnabaHelper(PredictAbstract):
    def __init__(self, *args, **kwargs):
        super(BarnabaHelper, self).__init__(name="barnaba",*args, **kwargs)

    @staticmethod
    def compute_rmsd(
        pred_path: str,
        native_path: str,
    ) -> float:
        """
        Compute the RMSD from the baRNAba implementation
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the RMSD score
        """
        try:
            rmsd_score = bb.rmsd(native_path, pred_path)[0]
            rmsd_score = round(float(rmsd_score), 3)
        except AssertionError:
            rmsd_score = np.nan
        return rmsd_score

    @staticmethod
    def compute_ermsd(
        pred_path: str,
        native_path: str,
    ) -> float:
        """
        Compute the eRMSD from the baRNAba implementation
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the eRMSD score
        """
        try:
            ermsd_score = bb.ermsd(native_path, pred_path)[0]
            ermsd_score = round(ermsd_score, 3)
        except AssertionError:
            ermsd_score = np.nan
        return ermsd_score

    @staticmethod
    def compute_escore(
        pred_path: str,
        native_path: str,
    ) -> float:
        """
        Compute the eScore from the baRNAba implementation
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the eScore
        """
        e_score_fit = escore.Escore([native_path])
        pred_escore = e_score_fit.score(pred_path)[0]
        pred_escore = round(pred_escore, 3)
        return pred_escore

    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Return the RMSD, eRMSD and eScore from baRNAba implementation
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: a dictionary with the 3 scores
        """
        rmsd, rmsd_time = fn_time(self.compute_rmsd, pred_path, native_path)
        ermsd, ermsd_time = fn_time(self.compute_ermsd, pred_path, native_path)
        e_score, e_score_time = fn_time(self.compute_escore, pred_path, native_path)
        scores = {"BARNABA-RMSD": rmsd, "BARNABA-eRMSD": ermsd, "BARNABA-eSCORE": e_score}
        times = {
            "BARNABA-RMSD": rmsd_time,
            "BARNABA-eRMSD": ermsd_time,
            "BARNABA-eSCORE": e_score_time,
        }
        return scores, times

main = build_predict_cli(BarnabaHelper)

if __name__ == "__main__":
    main()
