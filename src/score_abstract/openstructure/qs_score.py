from typing import Tuple, Dict

from src.score_abstract.openstructure.abstract_ost import AbstractOST
from src.utils import time_it


class QSScore(AbstractOST):
    """
    Compute qs-score using the OpenStructure library.
    """

    def __init__(self, *args, **kwargs):
        super(QSScore, self).__init__(*args, **kwargs)

    @time_it
    def _compute(self, pred_path: str, native_path: str) -> Tuple[Dict, Dict]:
        """
        Compute the qs-score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the qs-score
        """
        qs_score = self.compute_qs_score(pred_path, native_path)
        return {"QS-score": qs_score}  # type: ignore

    @staticmethod
    def compute_qs_score(pred_path: str, native_path: str) -> float:
        """
        Compute the QS-score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the QS-score for the prediction.
        """
        return AbstractOST.get_metric(pred_path, native_path, "qs-score")
