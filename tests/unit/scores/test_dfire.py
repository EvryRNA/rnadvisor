"""
File that test the DFIRE-RNA score
"""
import os
import unittest

from src.score_abstract.dfire.score_dfire import ScoreDfire

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

DFIRE1, DFIRE2 = -83024.952, -84146.064
class TestDfire(unittest.TestCase):
    def test_dfire(self):
        dfire1 = ScoreDfire.compute_dfire(STRUCT1)
        dfire2 = ScoreDfire.compute_dfire(STRUCT2)
        self.assertEqual(dfire1, DFIRE1)
        self.assertEqual(dfire2, DFIRE2)
