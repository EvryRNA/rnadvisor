"""
Class that computes the lDDT score from OpenStructure Library.

The original code can be found at the following website:
https://git.scicore.unibas.ch/schwede/openstructure/-/tree/master?ref_type=heads

Source for the lDDT score:
    Mariani, V., Biasini, M., Barbato, A., & Schwede, T. (2013).
    lDDT: a local superposition-free score for comparing protein structures and models
    using distance difference tests.
    Bioinformatics (Oxford, England), 29(21), 2722–2728.
    https://doi.org/10.1093/bioinformatics/btt473
"""
from typing import Tuple, Dict


from src.score_abstract.openstructure.abstract_ost import AbstractOST
from src.score_abstract.score_abstract import ScoreAbstract
from src.utils import time_it


class ScorelDDT(ScoreAbstract):
    def __init__(self, *args, **kwargs):
        """
        Compute the lDDT score using the OpenStructure library.
        """
        super(ScorelDDT, self).__init__(*args, **kwargs)

    @time_it
    def _compute(self, pred_path: str, native_path: str) -> Tuple[Dict, Dict]:
        """
        Compute the lDDT for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the lDDT score
        """
        lddt_score = self.compute_lddt(pred_path, native_path)
        return {"lDDT": lddt_score}  # type: ignore

    @staticmethod
    def compute_lddt(pred_path: str, native_path: str) -> float:
        """
        Compute the lDDT score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the lDDT score for the prediction.
        """
        return AbstractOST.get_metric(pred_path, native_path, "lddt")
