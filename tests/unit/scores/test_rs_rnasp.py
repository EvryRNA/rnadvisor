"""Class that implements the test for the rsRNASP scores."""
import os
import unittest

from src.score_abstract.rs_rnasp.score_rs_rnasp import ScoreRsRNASP

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

rs_RASP1, rs_RASP2 = -12705.015, -11549.93

class TestRsRNASP(unittest.TestCase):
    def test_rs_rnasp(self):
        rs_rasp1 = ScoreRsRNASP.compute_rs_rnasp(STRUCT1)
        rs_rasp2 = ScoreRsRNASP.compute_rs_rnasp(STRUCT2)
        self.assertTrue(rs_rasp1, rs_RASP1)
        self.assertTrue(rs_rasp2, rs_RASP2)
