"""
File that compute the RMSD between two molecules.
This is based on the https://github.com/RNA-Puzzles/RNA_assessment
To center the two molecules, it uses the Kabsch algorithm:
Kabsch W., 1976, A solution for the best rotation to relate two sets of vectors,
Acta Crystallographica, A32:922-923, doi: http://dx.doi.org/10.1107/S0567739476001873
"""

from typing import Dict, Optional, Tuple

from lib.rna_assessment.RNA_normalizer.structures.pdb_comparer import PDBComparer
from lib.rna_assessment.RNA_normalizer.structures.pdb_struct import PDBStruct

from rnadvisor.metric.rna_assessment.abstract_assessment import AbstractAssessment
from rnadvisor.utils.utils import time_it

from rnadvisor.cli_runner import build_predict_cli


class RMSDHelper(AbstractAssessment):
    def __init__(self, *args, **kwargs):
        super(RMSDHelper, self).__init__(name="RMSD", *args, **kwargs)

    @time_it
    def _compute_from_structure(
        self, native_struc: PDBStruct, pred_struc: PDBStruct
    ) -> Tuple[Dict, Dict]:
        """
        Compute the RMSD score from the native and predicted structures.
        Return in a dictionary format.
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: the RMSD score from these structures
        """
        rmsd = self.compute_rmsd_from_structures(native_struc, pred_struc)
        return {self.name: rmsd}  # type: ignore

    @staticmethod
    def compute_rmsd_from_structures(native_struc: PDBStruct, pred_struc: PDBStruct) -> float:
        """
        Static method to compute the RMSD score from the native and predicted structures.
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: the RMSD score from these structures
        """
        comparer = PDBComparer()
        rmsd = comparer.rmsd(src_struct=pred_struc, trg_struct=native_struc)
        return rmsd

    @staticmethod
    def compute_rmsd(
        pred_path: str,
        native_path: str,
        native_index: Optional[str] = None,
        prediction_index: Optional[str] = None,
    ) -> float:
        """
        Static method to compute the RMSD score from the native and predicted structures.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :return: the RMSD score from these structures
        """
        native_struc, pred_struc = AbstractAssessment.convert_pdb_to_structure(
            pred_path, native_path, native_index, prediction_index
        )
        rmsd = RMSDHelper.compute_rmsd_from_structures(native_struc, pred_struc)
        return rmsd

main = build_predict_cli(RMSDHelper)

if __name__ == "__main__":
    main()
