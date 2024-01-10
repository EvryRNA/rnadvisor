"""Class that implements the test for the ARES score."""
import os
import unittest

from src.score_abstract.ares.score_ares import ScoreARES

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

ARES_1, ARES_2 = 5.68, 5.522

class TestARES(unittest.TestCase):
    def test_ares(self):
        ares_1 = ScoreARES.compute_ares(STRUCT1)
        ares_2 = ScoreARES.compute_ares(STRUCT2)
        self.assertTrue(ARES_1, ares_1)
        self.assertTrue(ARES_2, ares_2)
