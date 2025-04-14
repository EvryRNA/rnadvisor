"""
Class that runs the LociPARSE score.
The original github code is the following:
    https://github.com/Bhattacharya-Lab/lociPARSE
The original paper is:
Tarafder S, Bhattacharya D.
lociPARSE: A Locality-aware Invariant Point Attention Model for Scoring RNA 3D Structures.
J Chem Inf Model.
2024 Nov 25;64(22):8655-8664. doi: 10.1021/acs.jcim.4c01621.
Epub 2024 Nov 11. PMID: 39523843; PMCID: PMC11600500.
"""
from typing import Optional, Tuple, Dict

import numpy as np
from lociPARSE import lociparse

from rnadvisor.predict_abstract import PredictAbstract

from rnadvisor.cli_runner import build_predict_cli

from rnadvisor.utils.utils import time_it


class LOCIPARSEHelper(PredictAbstract):
    def __init__(self, *args, **kwargs):
        super().__init__(name="LociPARSE", *args, **kwargs)


    def compute_lociparse(self, pred_path: str) -> float:
        """
        Compute the LociPARSE score for a given structure.
        :param pred_path: the path to the .pdb file of a prediction.
        :return: the LociPARSE score of the pred file
        """
        lp = lociparse()
        try:
            score = lp.score(pred_path)
        except (ValueError, UnboundLocalError):
            return np.nan
        return score.pMoL.value

    @time_it
    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the LociPARSE score for a given structure.
        :param pred_path: the path to the .pdb file of a prediction.
        :return: LociPARSE
        """
        lociparse_score = self.compute_lociparse(pred_path)
        return {self.name: lociparse_score}  # type: ignore

main = build_predict_cli(LOCIPARSEHelper)

if __name__ == "__main__":
    main()
