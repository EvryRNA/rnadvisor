"""Class that wraps all the scores into one interface"""
import os
from abc import abstractmethod
from typing import Dict, List, Optional, Tuple

from loguru import logger


class ScoreAbstract:
    def __init__(
        self,
        pred_path: Optional[List[str]] = None,
        native_path: Optional[str] = None,
        *args,
        **kwargs,
    ):
        """
        Initialise the score class that interfaces all the different metrics.
        :param pred_path: list of paths to .pdb predictions
        :param native_path: path to the native .pdb file
        """
        self.pred_path = pred_path
        self.native_path = native_path

    def compute(
        self, pred_paths: Optional[List[str]], native_path: Optional[str]
    ) -> Tuple[Dict, Dict]:
        """
        Compute the given score for the list of predictions, and give the computation time.
        :param pred_paths: list of path to .pdb predictions. If None, set to the class variable.
        :param native_path: path to the native .pdb file. If None, set to the class variable.
        :return: a dictionary with the score for the given predictions.
        """
        pred_paths = self.pred_path if pred_paths is None else pred_paths
        native_path = self.native_path if native_path is None else native_path
        if pred_paths is None or native_path is None:
            return {}, {}
        scores: Dict = {}
        times: Dict = {}
        for sub_path in pred_paths:
            if self.check_pdb_file(in_path=sub_path):
                c_scores, c_times = self._compute(sub_path, native_path)
                for score_n, score in c_scores.items():
                    if sub_path in scores:
                        scores[sub_path][score_n] = score
                        times[sub_path][score_n] = c_times[score_n]
                    else:
                        scores[sub_path] = {score_n: score}
                        times[sub_path] = {score_n: c_times[score_n]}
            else:
                logger.debug(f"FILE {sub_path} EITHER DOESN'T EXIST OR ISN'T A .pdb FILE")
        return scores, times

    @staticmethod
    def check_pdb_file(in_path: str) -> bool:
        """
        Check if the file exists and if this is a .pdb file
        :param in_path: the path to a .pdb file
        :return: True if the file exists and is a .pdb file
        """
        return os.path.exists(in_path) and in_path.endswith(".pdb")

    @abstractmethod
    def _compute(self, pred_path: str, native_path: str) -> Tuple[Dict, Dict]:
        """
        Compute the score for a given prediction and the native .pdb path.
        It returns also the time needed to compute the score.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: dictionary with the scores and the given values for the inputs
        """
        raise NotImplementedError
