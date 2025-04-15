"""
Class that implements the Deformation Index score.
It uses the RNA_Assessment repo.
"""

from typing import Dict, Optional, Tuple

import numpy as np
from lib.rna_assessment.RNA_normalizer.structures.pdb_struct import PDBStruct
from loguru import logger

from rnadvisor.metric.rna_assessment.abstract_assessment import AbstractAssessment
from rnadvisor.metric.rna_assessment.inf_helper import INFHelper
from rnadvisor.metric.rna_assessment.rmsd_helper import RMSDHelper
from rnadvisor.utils.utils import time_it

from rnadvisor.cli_runner import build_predict_cli


class DIHelper(AbstractAssessment):
    def __init__(self, *args, **kwargs):
        super(DIHelper, self).__init__(name="DI",*args, **kwargs)

    @staticmethod
    def compute_di_from_structures(native_struc: PDBStruct, pred_struc: PDBStruct) -> float:
        """
        Static method to compute the Deformation Index score
                from the native and predicted structures.
        This is defined as the RMSD / INF_all
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: the DI score from these structures
        """
        rmsd = RMSDHelper.compute_rmsd_from_structures(native_struc, pred_struc)
        inf_all = INFHelper.compute_inf_all_from_structures(native_struc, pred_struc)
        try:
            di = rmsd / inf_all
        except TypeError:
            logger.debug(f"ERROR IN DI SCORE : RMSD {rmsd} AND INF_ALL : {inf_all}")
            di = np.nan
        return di

    @staticmethod
    def compute_di(
        pred_path: str,
        native_path: str,
        native_index: Optional[str] = None,
        prediction_index: Optional[str] = None,
    ) -> float:
        """
        Static method to compute the Deformation Index score
                from the native and predicted structures.
        This is defined as the RMSD / INF_all
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :return: the DI score from these structures
        """
        native_struc, pred_struc = AbstractAssessment.convert_pdb_to_structure(
            pred_path, native_path, native_index, prediction_index
        )
        di = DIHelper.compute_di_from_structures(native_struc, pred_struc)
        return di

    @time_it
    def _compute_from_structure(
        self, native_struc: PDBStruct, pred_struc: PDBStruct
    ) -> Tuple[Dict, Dict]:
        """
        Compute the DI score from the native and predicted structures.
        Return in a dictionary format.
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: the DI score from these structures
        """
        di = self.compute_di_from_structures(native_struc, pred_struc)
        return {"DI": di}  # type: ignore

main = build_predict_cli(DIHelper)

if __name__ == "__main__":
    main()
