"""Class that does the tests for the Zhanggroup code"""
import os
import unittest

from src.score_abstract.score_zhanggroup.tm_gdt_scores import GdtScores

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

TRUE_SCORES= {
    "GDT-TS": 0.3713,
    "GDT-TS-DETAILED": {
        'GDT-TS@1': 0.1683, 'GDT-TS@2': 0.297, 'GDT-TS@4': 0.4158, 'GDT-TS@8': 0.604
    }
}
class TestZhanggroupScores(unittest.TestCase):
    """Unit test for GDT-TS score"""

    def test_gdt_ts(self):
        gts_score = GdtScores.compute_gdt_ts(STRUCT1, STRUCT2)
        self.assertAlmostEqual(gts_score, TRUE_SCORES['GDT-TS'])

    def test_gdt_ts_detailed(self):
        gdt_ts_detailed = GdtScores.compute_gdt_ts_detailed(STRUCT1, STRUCT2)
        self.assertAlmostEqual(gdt_ts_detailed, TRUE_SCORES['GDT-TS-DETAILED'])