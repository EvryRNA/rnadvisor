from typing import Tuple, Dict

from src.score_abstract.openstructure.abstract_ost import AbstractOST
from src.utils import time_it


class TMScore(AbstractOST):
    """
    Compute TM-score using the OpenStructure library.
    """

    def __init__(self, *args, **kwargs):
        super(TMScore, self).__init__(*args, **kwargs)

    @time_it
    def _compute(self, pred_path: str, native_path: str, *args, **kwargs) -> Tuple[Dict, Dict]:
        """
        Compute the TM-score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the TM-score
        """
        tm_score = self.compute_tm_score(pred_path, native_path)
        return {"TM-score (OST)": tm_score}  # type: ignore

    @staticmethod
    def compute_tm_score(pred_path: str, native_path: str) -> float:
        """
        Compute the TM-score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the TM-score for the prediction.
        """
        return AbstractOST.get_metric(pred_path, native_path, "tm-score")
