"""
Class that get and convert the pdb files to structures encoded by RNA-tools.
"""

import os
from typing import Dict, Optional, Tuple

from lib.rna_assessment.RNA_normalizer.structures.pdb_struct import PDBStruct

from rnadvisor.predict_abstract import PredictAbstract

class AbstractAssessment(PredictAbstract):
    def __init__(self, mc_annotate_bin: Optional[str] = None, *args, **kwargs):
        """
        :param mc_annotate_bin: path to the binary MC-Annotate file. Default in `config.py` file.
        """
        super(AbstractAssessment, self).__init__(*args, **kwargs)
        self.mc_annotate_bin = (
            mc_annotate_bin
            if mc_annotate_bin is not None
            else os.path.join("lib", "rna_assessment", "MC-Annotate")
        )

    @staticmethod
    def convert_pdb_to_structure(
        pred_path: str,
        native_path: str,
        native_index: Optional[str] = None,
        prediction_index: Optional[str] = None,
        mc_annotate_bin: Optional[str] = None,
    ) -> Tuple[PDBStruct, PDBStruct]:
        """
        Convert the .pdb files to structures readable by RNA-tools.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :param native_index: file that describes the delimitation of the RNA for the native file
        :param prediction_index: file that describes the delimitation of the RNA
                    for the prediction file
        :param mc_annotate_bin: path to the binary MC-Annotate file. Default in `config.py` file.
        :return: two instances of PDBStruct for the native and prediction structures
        """
        native_struc, pred_struc = PDBStruct(mc_annotate_bin), PDBStruct(mc_annotate_bin)
        native_struc.load(native_path, native_index)
        pred_struc.load(pred_path, prediction_index)
        return native_struc, pred_struc

    def _compute_from_structure(
        self, native_struc: PDBStruct, pred_struc: PDBStruct
    ) -> Tuple[Dict, Dict]:
        """
        Compute a given score from the native and predicted structures.
        :param native_struc: native structure in a PDBStruc instance
        :param pred_struc: predicted structure in a PDBStruc instance
        :return: a dictionary with the name of the score and the value
        """
        raise NotImplementedError

    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
        ) -> Tuple[Dict, Dict]:
        """
        Compute a give score from the prediction and a native structure
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return:
        """
        native_struc, pred_struc = self.convert_pdb_to_structure(
            pred_path, native_path, mc_annotate_bin=self.mc_annotate_bin
        )
        return self._compute_from_structure(native_struc, pred_struc)
