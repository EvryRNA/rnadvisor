"""
Class that computes the CAD (Contact Area Difference) score using the implementation of voronota.
The source code of Voronota is available at:
    https://github.com/kliment-olechnovic/voronota
The associated paper is the following:
    Kliment Olechnovič, Česlovas Venclovas,
    The CAD-score web server: contact area-based comparison of structures and interfaces
    of proteins, nucleic acids and their complexes,
    Nucleic Acids Research, Volume 42, Issue W1, 1 July 2014,
    Pages W259–W263, https://doi.org/10.1093/nar/gku294
"""

import subprocess
from typing import Dict, Tuple, Optional

import numpy as np


from rnadvisor.predict_abstract import PredictAbstract


from rnadvisor.cli_runner import build_predict_cli

from rnadvisor.utils.utils import time_it


class CADScoreHelper(PredictAbstract):
    def __init__(self, *args, **kwargs):
        super(CADScoreHelper, self).__init__(name="CAD",*args, **kwargs)

    @staticmethod
    def compute_cad_score(
        pred_path: str,
        native_path: str,
    ) -> float:
        """
        Compute the CAD score using the voronota implementation.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: return the CAD score using bash command
        """
        # Get the shell command that will be executed
        command = (
            f"voronota-cadscore --input-target {native_path} --input-model {pred_path}"
            + "| awk '{print $5}'"
        )
        output = subprocess.check_output(command, shell=True)
        try:
            cad_score = float(str(output.decode()).replace("\n", ""))
        except ValueError:
            cad_score = np.nan
        if cad_score == 0:
            cad_score = np.nan
        return cad_score

    @time_it
    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the CAD score for a given prediction and the native .pdb path.
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: dictionary with the CAD score for the given inputs
        """
        mcq_score = self.compute_cad_score(pred_path, native_path)
        return {"CAD": mcq_score}  # type: ignore

main = build_predict_cli(CADScoreHelper)

if __name__ == "__main__":
    main()
