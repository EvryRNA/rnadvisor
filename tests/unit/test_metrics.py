import os
import unittest
from typing import Optional

import pandas as pd
import pandas.testing as pdt

from rnadvisor.rnadvisor_cli import RNAdvisorCLI

PRED_DIR = os.path.join("tests", "data", "input")
NATIVE_PATH = os.path.join("tests", "data", "input", "native.pdb")
OUT_DIR = os.path.join("tests", "data", "output")

df_true = pd.read_csv(os.path.join(OUT_DIR, "out.csv"), index_col=[0])
df_true_sorted = df_true.sort_index()


class TestMetrics(unittest.TestCase):
    def get_score(self, name: str):
        rnadvisor_cli = RNAdvisorCLI(
            pred_dir=PRED_DIR,
            native_path=NATIVE_PATH,
            scores=[name],
            params={"mcq_threshold": [10, 15, 20, 25], "mcq_mode": 2},
        )
        df = rnadvisor_cli.predict()
        return df

    def _test_score(self, name: str, df_name: Optional[str] = None):
        df, _ = self.get_score(name)
        df = df.sort_index()
        df_sorted = df.sort_index()
        df_name = name if df_name is None else df_name
        pdt.assert_frame_equal(df_sorted, df_true_sorted[df_name])

    def test_mcq(self):
        self._test_score("mcq", ["MCQ"])

    def test_lcs(self):
        self._test_score(
            "lcs",
            [
                "LCS-TA-COVERAGE-10",
                "LCS-TA-RESIDUES-10",
                "LCS-TA-COVERAGE-15",
                "LCS-TA-RESIDUES-15",
                "LCS-TA-COVERAGE-20",
                "LCS-TA-RESIDUES-20",
                "LCS-TA-COVERAGE-25",
                "LCS-TA-RESIDUES-25",
            ],
        )

    def test_lddt(self):
        self._test_score("lddt", ["lddt", "C-lddt"])

    def test_tm_score(self):
        self._test_score("tm-score", ["TM-score"])

    def test_rmsd(self):
        self._test_score("rmsd", ["RMSD"])

    def test_inf(self):
        self._test_score("inf", ["INF-ALL", "INF-WC", "INF-NWC", "INF-STACK"])

    def test_p_value(self):
        self._test_score("p-value", ["P-VALUE"])

    def test_di(self):
        self._test_score("di", ["DI"])

    def test_gdt_ts(self):
        self._test_score(
            "gdt-ts", ["GDT-TS", "GDT-TS@1", "GDT-TS@2", "GDT-TS@4", "GDT-TS@8"]
        )

    def test_cad_score(self):
        self._test_score("cad-score", ["CAD"])


if __name__ == "__main__":
    unittest.main()
