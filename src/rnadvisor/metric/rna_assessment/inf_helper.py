"""
Class that computes the INF score.
This is based on the RNA-tools implementation.
The INF score was invented to assess the central characteristics of RNA architecture.
The INF can either measure different interaction types
    (WC base-pairing, non-WC base pairing, base stacking) separately or combine
    all of the types (resulting in INFwc, INFnwc, INFstacking and INFall)
"""

from typing import Dict, Optional, Tuple
import numpy as np

from lib.rna_assessment.RNA_normalizer.structures.pdb_comparer import PDBComparer
from lib.rna_assessment.RNA_normalizer.structures.pdb_struct import PDBStruct

from rnadvisor.metric.rna_assessment.abstract_assessment import AbstractAssessment
from rnadvisor.utils.utils import fn_time

from rnadvisor.cli_runner import build_predict_cli


class INFHelper(AbstractAssessment):
    def __init__(self, *args, **kwargs):
        super(INFHelper, self).__init__(name="INF", *args, **kwargs)

    @staticmethod
    def compute_inf_all_from_structures(native_struc: PDBStruct, pred_struc: PDBStruct) -> float:
        """
        Compute the INF score combining all the types.
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: the INF score of the associated molecules
        """
        comparer = PDBComparer()
        inf_all = comparer.INF(src_struct=pred_struc, trg_struct=native_struc, type="ALL")
        if inf_all == -1:
            inf_all = np.nan
        return inf_all

    @staticmethod
    def compute_inf_all(
            pred_path: str,
            native_path: str,
            native_index: Optional[str] = None,
            prediction_index: Optional[str] = None,
    ) -> float:
        """
        Compute the INF score combining all the types.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :return: the INF score of the associated molecules
        """
        native_struc, pred_struc = AbstractAssessment.convert_pdb_to_structure(
            pred_path, native_path, native_index, prediction_index
        )
        inf_all = INFHelper.compute_inf_all_from_structures(native_struc, pred_struc)
        return inf_all

    @staticmethod
    def compute_inf_wc_from_structures(native_struc: PDBStruct, pred_struc: PDBStruct) -> float:
        """
        Compute the INF score only for the WC base-pairing
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: the INFwc score of the associated molecules
        """
        comparer = PDBComparer()
        inf_wc = comparer.INF(src_struct=pred_struc, trg_struct=native_struc, type="PAIR_2D")
        if inf_wc == -1:
            inf_wc = np.nan
        return inf_wc

    @staticmethod
    def compute_inf_wc(
            pred_path: str,
            native_path: str,
            native_index: Optional[str] = None,
            prediction_index: Optional[str] = None,
    ) -> float:
        """
        Compute the INF score only for the WC base-pairing
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :return: the INFwc score of the associated molecules
        """
        native_struc, pred_struc = AbstractAssessment.convert_pdb_to_structure(
            pred_path, native_path, native_index, prediction_index
        )
        inf_wc = INFHelper.compute_inf_wc_from_structures(native_struc, pred_struc)
        return inf_wc

    @staticmethod
    def compute_inf_nwc_from_structures(native_struc: PDBStruct, pred_struc: PDBStruct) -> float:
        """
        Compute the INF score only for the non WC base-pairing
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: the INFwc score of the associated molecules
        """
        comparer = PDBComparer()
        inf_nwc = comparer.INF(src_struct=pred_struc, trg_struct=native_struc, type="PAIR_3D")
        if inf_nwc == -1:
            inf_nwc = np.nan
        return inf_nwc

    @staticmethod
    def compute_inf_nwc(
            pred_path: str,
            native_path: str,
            native_index: Optional[str] = None,
            prediction_index: Optional[str] = None,
    ) -> float:
        """
        Compute the INF score only for the non WC base-pairing
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :return: the INFwc score of the associated molecules
        """
        native_struc, pred_struc = AbstractAssessment.convert_pdb_to_structure(
            pred_path, native_path, native_index, prediction_index
        )
        inf_nwc = INFHelper.compute_inf_nwc_from_structures(native_struc, pred_struc)
        return inf_nwc

    @staticmethod
    def compute_inf_stack_from_structures(native_struc: PDBStruct, pred_struc: PDBStruct) -> float:
        """
        Compute the INF score only for the non WC base-pairing
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: the INFwc score of the associated molecules
        """
        comparer = PDBComparer()
        inf_stack = comparer.INF(src_struct=pred_struc, trg_struct=native_struc, type="STACK")
        if inf_stack == -1:
            inf_stack = np.nan
        return inf_stack

    @staticmethod
    def compute_inf_stack(
            pred_path: str,
            native_path: str,
            native_index: Optional[str] = None,
            prediction_index: Optional[str] = None,
    ) -> float:
        """
        Compute the INF score only for the non WC base-pairing
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :return: the INFwc score of the associated molecules
        """
        native_struc, pred_struc = AbstractAssessment.convert_pdb_to_structure(
            pred_path, native_path, native_index, prediction_index
        )
        inf_stack = INFHelper.compute_inf_stack_from_structures(native_struc, pred_struc)
        return inf_stack

    def _compute_from_structure(
            self, native_struc: PDBStruct, pred_struc: PDBStruct
    ) -> Tuple[Dict, Dict]:
        """
        Compute a the INF scores from the structures
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: a dictionary with the INF_all, INF_wc, INF_nwc and INF_stack
        """
        inf_all, times_inf_all = fn_time(
            self.compute_inf_all_from_structures,
            native_struc,
            pred_struc,
        )
        inf_wc, times_inf_wc = fn_time(
            self.compute_inf_wc_from_structures,
            native_struc,
            pred_struc,
        )
        inf_nwc, times_inf_nwc = fn_time(
            self.compute_inf_nwc_from_structures,
            native_struc,
            pred_struc,
        )
        inf_stack, times_inf_stack = fn_time(
            self.compute_inf_stack_from_structures,
            native_struc,
            pred_struc,
        )
        scores = {"INF-ALL": inf_all, "INF-WC": inf_wc, "INF-NWC": inf_nwc, "INF-STACK": inf_stack}
        times = {
            "INF-ALL": times_inf_all,
            "INF-WC": times_inf_wc,
            "INF-NWC": times_inf_nwc,
            "INF-STACK": times_inf_stack,
        }
        return scores, times

main = build_predict_cli(INFHelper)

if __name__ == "__main__":
    main()
