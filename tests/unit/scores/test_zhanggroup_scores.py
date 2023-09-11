"""Class that does the tests for the Zhanggroup code"""
import os
import unittest

from src.score_abstract.score_zhanggroup.tm_gdt_scores import TmGdtScores

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

TRUE_SCORES= {
    "TM-SCORE": 0.342,
    "GDT-TS": 0.3713,
    "GDT-TS-DETAILED": {
        'GDT-TS@1': 0.1683, 'GDT-TS@2': 0.297, 'GDT-TS@4': 0.4158, 'GDT-TS@8': 0.604
    }
}
class TestZhanggroupScores(unittest.TestCase):
    """Unit test for TM-score and GDT-TS score"""

    def test_tm_score(self):
        tm_pred = TmGdtScores.compute_tm_score(STRUCT1, STRUCT2)
        self.assertAlmostEqual(tm_pred, TRUE_SCORES['TM-SCORE'])

    def test_gdt_ts(self):
        gts_score = TmGdtScores.compute_gdt_ts(STRUCT1, STRUCT2)
        self.assertAlmostEqual(gts_score, TRUE_SCORES['GDT-TS'])

    def test_gdt_ts_detailed(self):
        gdt_ts_detailed = TmGdtScores.compute_gdt_ts_detailed(STRUCT1, STRUCT2)
        self.assertAlmostEqual(gdt_ts_detailed, TRUE_SCORES['GDT-TS-DETAILED'])