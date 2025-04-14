"""
Class that runs the TorsionBERT-MCQ score
The original github code is the following:
    https://github.com/EvryRNA/RNA-TorsionBERT
The original paper is:
Clément Bernard, Guillaume Postic, Sahar Ghannay, Fariza Tahi,
RNA-TorsionBERT: leveraging language models for RNA 3D torsion angles prediction,
Bioinformatics, Volume 41, Issue 1, January 2025, btaf004,
https://doi.org/10.1093/bioinformatics/btaf004
"""
from typing import Optional, List, Tuple, Dict

import numpy as np
import torch
from rna_torsionbert.tb_mcq_cli import TBMCQCLI


from rnadvisor.utils.utils import time_it

from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract

class TBMCQHelper(PredictAbstract):
    def __init__(self, *args, **kwargs):
        super().__init__(name="tb_mcq", *args, **kwargs)

    def compute_tbmcq(self, pred_path: str) -> float:
        try:
            mcq = self.tb_mcq.compute_tb_mcq(pred_path)
        except ValueError:
            mcq = np.nan
        return mcq

    @time_it
    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the TorsionBERT-MCQ score for a given structure.
        :param pred_path: the path to the .pdb file of a prediction.
        :return: tb-mcq
        """
        score = self.compute_tbmcq(pred_path)
        return {self.name: score}  # type: ignore

    def prepare_data(self, native_path: Optional[str], pred_paths: List[str], *args, **kwargs):
        """
        Prepare the data for the metric/scoring function.
        It can be the load of the model or the preprocessing of the data.
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_paths: list of paths to RNA `.pdb` files.
        """
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tb_mcq = TBMCQCLI(None, None, device)

main = build_predict_cli(TBMCQHelper)

if __name__ == "__main__":
    main()