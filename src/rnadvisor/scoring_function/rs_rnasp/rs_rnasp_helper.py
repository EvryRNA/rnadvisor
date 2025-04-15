"""
Class that implements the rsRNASP score.

Original code from:
https://github.com/Tan-group/rsRNASP

I created a fork with only the needed files:
https://github.com/clementbernardd/rsRNASP/tree/scoring-version

Original paper:
Tan YL, Wang X, Shi YZ, Zhang W, Tan ZJ.
2022.
rsRNASP: A residue-separation-based statistical potential for RNA 3D structure
evaluation. Biophys J. 121: 142-156.
"""

import os
import subprocess
from typing import Dict, List, Optional, Tuple


from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract

from rnadvisor.utils.utils import time_it


class RsRNASPHelper(PredictAbstract):
    """
    Class that implements the rsRNASP code from the official github page.
    """

    def __init__(self, rs_rnasp_bin_path: Optional[str] = None, *args, **kwargs):
        super(RsRNASPHelper, self).__init__(name="rsRNASP",*args, **kwargs)
        self.rs_rnasp_bin_path = rs_rnasp_bin_path

    @staticmethod
    def compute_rs_rnasp(pred_path: str, rs_rnasp_bin_path: Optional[str] = None) -> List:
        """
        Compute the rsRNASP energy.
        :param pred_path: path to a .pdb file
        :param rs_rnasp_bin_path: binary path to the rasp_fd file
        :return: the rsRNASP score
        """
        rs_rnasp_bin_path = (
            rs_rnasp_bin_path
            if rs_rnasp_bin_path is not None
            else os.path.join("lib", "rs_rnasp", "rsRNASP")
        )
        command = f"{rs_rnasp_bin_path} {pred_path}"
        output = subprocess.check_output(command, shell=True)
        rs_rnasp = output.decode().replace("\n", "")
        rs_rnasp = round(float(rs_rnasp), 3)  # type: ignore
        return rs_rnasp  # type: ignore

    @time_it
    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        rs_rnasp = self.compute_rs_rnasp(pred_path, self.rs_rnasp_bin_path)
        return {"rsRNASP": rs_rnasp}  # type: ignore

main = build_predict_cli(RsRNASPHelper)

if __name__ == "__main__":
    main()
