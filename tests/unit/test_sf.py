import os
import unittest
from typing import Optional

import pandas as pd
import pandas.testing as pdt

from rnadvisor.rnadvisor_cli import RNAdvisorCLI

PRED_DIR = os.path.join("tests", "data", "input")
OUT_DIR = os.path.join("tests", "data", "output")

df_true = pd.read_csv(os.path.join(OUT_DIR, "out.csv"), index_col=[0])
df_true_sorted = df_true.sort_index()


class TestSF(unittest.TestCase):
    def get_score(self, name: str):
        rnadvisor_cli = RNAdvisorCLI(pred_dir=PRED_DIR, scores=[name])
        df = rnadvisor_cli.predict()
        return df

    def _test_score(self, name: str, df_name: Optional[str] = None):
        df, _ = self.get_score(name)
        df = df.sort_index()
        df_sorted = df.sort_index()
        df_name = name if df_name is None else df_name
        pdt.assert_frame_equal(df_sorted, df_true_sorted[df_name])

    def test_3drnascore(self):
        self._test_score("3drnascore", ["3drnascore"])

    def test_lociparse(self):
        self._test_score("lociparse", ["LociPARSE"])

    def test_tbmcq(self):
        self._test_score("tb-mcq", ["tb_mcq"])

    def test_escore(self):
        self._test_score("escore", ["BARNABA-eSCORE"])

    def test_pamnet(self):
        self._test_score("pamnet", ["PAMNet"])

    def test_cgrnasp(self):
        self._test_score("cgrnasp", ["cgRNASP", "cgRNASP-C", "cgRNASP-PC"])

    def test_dfire(self):
        self._test_score("dfire", ["DFIRE"])

    def test_rasp(self):
        self._test_score(
            "rasp", ["rasp-energy", "rasp-nb-contacts", "rasp-normalized-energy"]
        )

    def test_rsrnasp(self):
        self._test_score("rs-rnasp", ["rsRNASP"])

    def test_ares(self):
        self._test_score("ares", ["ARES"])


if __name__ == "__main__":
    unittest.main()
