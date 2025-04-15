"""
File that computes the p-value score. This is based on the RNA-Assessment implementation:
 https://github.com/RNA-Puzzles/RNA_assessment/blob/master
It uses the formula given in the following paper:
Hajdin, C. E., Ding, F., Dokholyan, N. v., & Weeks, K. M. (2010).
On the significance of an RNA tertiary structure prediction.
RNA, 16(7), 1340–1349. https://doi.org/10.1261/rna.1837410
They suggest the following rule:
    P < 0.01 represents a successful prediction
They also explain that the P-value with their formula makes sense for RNAs sequence between
                35 and 161 nucleotides.
"""

from typing import Dict, Optional, Tuple

import numpy as np
from lib.rna_assessment.RNA_normalizer.structures.pdb_comparer import PDBComparer
from lib.rna_assessment.RNA_normalizer.structures.pdb_struct import PDBStruct
from loguru import logger


from rnadvisor.metric.rna_assessment.abstract_assessment import AbstractAssessment
from rnadvisor.metric.rna_assessment.rmsd_helper import RMSDHelper
from rnadvisor.utils.utils import time_it

from rnadvisor.cli_runner import build_predict_cli


class PValueHelper(AbstractAssessment):
    def __init__(self, p_value_param: str = "-", *args, **kwargs):
        """
        Initialise the ScorePValue class
        :param p_value_param: the parameter for the P-value used in the RNA-tools.
            This is either '-' or '+'. Default to '-'.
        :param args:
        :param kwargs:
        """
        super(PValueHelper, self).__init__(name="P-VALUE", *args, **kwargs)
        self.p_value_param = p_value_param

    @time_it
    def _compute_from_structure(
        self, native_struc: PDBStruct, pred_struc: PDBStruct
    ) -> Tuple[Dict, Dict]:
        """
        Compute the P-value associated with the RMSD score
            from the native and predicted structures.
        Return a dictionary with the name and the score associated
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: a score from these structures
        """
        pvalue = self.compute_p_value_from_structures(native_struc, pred_struc, self.p_value_param)
        return {"P-VALUE": pvalue}  # type: ignore

    @staticmethod
    def compute_p_value(
        pred_path: str,
        native_path: str,
        native_index: Optional[str] = None,
        prediction_index: Optional[str] = None,
        p_value_param: str = "-",
    ) -> float:
        """
        Static method to compute the P-value associated with the RMSD score
                from the native and predicted structures.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :param p_value_param: the parameter for the P-value used in the RNA-tools.
            This is either '-' or '+'. Default to '-'.
        :return: a score from these structures
        """
        native_struc, pred_struc = AbstractAssessment.convert_pdb_to_structure(
            pred_path, native_path, native_index, prediction_index
        )
        pvalue = PValueHelper.compute_p_value_from_structures(
            native_struc, pred_struc, p_value_param
        )
        return pvalue

    @staticmethod
    def compute_p_value_from_structures(
        native_struc: PDBStruct, pred_struc: PDBStruct, p_value_param: str = "-"
    ) -> float:
        """
        Static method to compute the P-value associated with the RMSD score
                from the native and predicted structures.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :param p_value_param: the parameter for the P-value used in the RNA-tools.
            This is either '-' or '+'. Default to '-'.
        :return: a score from these structures
        """
        comparer = PDBComparer()
        rmsd = RMSDHelper.compute_rmsd_from_structures(
            native_struc=native_struc, pred_struc=pred_struc
        )
        raw_native_struc, raw_pred_structure = (
            native_struc.raw_sequence(),
            pred_struc.raw_sequence(),
        )
        if len(raw_native_struc) != len(raw_pred_structure):
            return np.nan
        if len(raw_pred_structure) <= 35 or len(raw_pred_structure) >= 161:
            logger.debug(
                f"P-VALUE NOT TRUSTABLE. THE LENGTH :{len(raw_pred_structure)} ISN'T "
                f"BETWEEN 35 and 161 AS MENTIONED IN THE ARTICLE"
            )
        pvalue = comparer.pvalue(rmsd, len(raw_native_struc), p_value_param)
        return pvalue

main = build_predict_cli(PValueHelper)

if __name__ == "__main__":
    main()
