"""
Class that runs the Clash score from RNAQUA.
The original github code is the following:
    https://github.com/mantczak/rnaqua
"""

import os
from typing import Dict, Optional, Tuple

import numpy as np

import xml.etree.ElementTree as ET

from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract

from rnadvisor.utils.utils import time_it

COMMAND = "$BIN_PATH --command CLASH-SCORE " \
          "--single-model-file-path $INPUT_PATH --output-file-path $OUTPUT_PATH 2>&1 > /dev/null"


class ClashHelper(PredictAbstract):
    def __init__(self, rnaqua_bin_path: Optional[str] = None, tmp_dir: str = os.path.join("tmp", "clash"),
                 *args, **kwargs):
        super(ClashHelper, self).__init__(name="CLASH", *args, **kwargs)
        self.rnaqua_bin_path = rnaqua_bin_path
        self.tmp_dir = tmp_dir
        os.makedirs(tmp_dir, exist_ok=True)

    @staticmethod
    def compute_clash(
        pred_path: str, tmp_path: str, rnaqua_bin_path: Optional[str] = None
    ) -> float:
        """
        Compute the Clash score for a given structure.
        :param pred_path: the path to the .pdb file of a prediction.
        :param tmp_path: the path to a temporary file to store the output.
        :param rnaqua_bin_path: the binary path to the rnaqua library
        :return: the Clash Score of the pred file
        """
        rnaqua_bin_path = (
            rnaqua_bin_path
            if rnaqua_bin_path is not None
            else os.path.join("lib", "rnaqua", "rnaqua-binary", "bin", "rnaqua.sh")
        )
        command = COMMAND.replace("$INPUT_PATH", pred_path).replace("$OUTPUT_PATH", tmp_path).replace("$BIN_PATH", rnaqua_bin_path)
        os.system(command)
        try:
            clash_score = ClashHelper.get_clash_score(tmp_path)
        except (ET.ParseError, FileNotFoundError):
            clash_score = np.nan
        if os.path.exists(tmp_path):
            os.system(f"rm {tmp_path}")
        return clash_score

    @staticmethod
    def get_clash_score(xml_file_path: str):
        """
        Extracts the clash score from the given XML file.
        """
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        score = root.find('.//score').text
        return float(score)

    @time_it
    def predict_single_file(
        self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        """
        Compute the Clash score for a given structure.
        :param pred_path: the path to the .pdb file of a prediction.
        :return: clash-score
        """
        tmp_out = os.path.join(self.tmp_dir, "tmp.xml")
        clash_score = self.compute_clash(pred_path, tmp_out, self.rnaqua_bin_path)
        return {self.name: clash_score}  # type: ignore

main = build_predict_cli(ClashHelper)

if __name__ == "__main__":
    main()
