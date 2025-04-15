from typing import Tuple, Dict, Optional

from rnadvisor.utils.utils import time_it
from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract

from rnadvisor.metric.open_structures.abstract_ost import AbstractOST

class TMScoreHelper(PredictAbstract):
    """
    Compute TM-score using the OpenStructure library.
    """

    def __init__(self, *args, **kwargs):
        super(TMScoreHelper, self).__init__(name = "tm-score-ost",*args, **kwargs)

    @time_it
    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the TM-score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the TM-score
        """
        tm_score = self.compute_tm_score(pred_path, native_path)
        return {"TM-score (OST)": tm_score[0]}  # type: ignore

    @staticmethod
    def compute_tm_score(pred_path: str, native_path: str) -> float:
        """
        Compute the TM-score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the TM-score for the prediction.
        """
        return AbstractOST.get_metric(pred_path, native_path, ["tm-score"])

main = build_predict_cli(TMScoreHelper)

if __name__ == "__main__":
    main()
