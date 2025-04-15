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

from typing import Tuple, Dict, Optional

from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract
from rnadvisor.utils.utils import fn_time

from rnadvisor.metric.open_structures.abstract_ost import AbstractOST


class LDDTHelper(PredictAbstract):
    def __init__(self, *args, **kwargs):
        """
        Compute the lDDT score using the OpenStructure library.
        """
        super(LDDTHelper, self).__init__(name="lddt", *args, **kwargs)

    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the lDDT for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the lDDT score
        """
        lddt_scores, lddt_time = fn_time(self.compute_lddt, pred_path, native_path)
        times = {self.name: lddt_time, f"C-{self.name}": lddt_time}
        scores = {self.name: lddt_scores[0], f"C-{self.name}": lddt_scores[1]}
        return scores, times

    @staticmethod
    def compute_lddt(pred_path: str, native_path: str) -> float:
        """
        Compute the lDDT score for a single prediction.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the lDDT score for the prediction.
        """
        return AbstractOST.get_metric(pred_path, native_path, ["lddt", "bb-lddt"])

main = build_predict_cli(LDDTHelper)

if __name__ == "__main__":
    main()
