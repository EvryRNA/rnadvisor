"""
Class that tests the baRNAba scores
"""
import os
import unittest

from src.score_abstract.barnaba.score_barnaba import ScoreBarnaba

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

RMSD, E_RMSD, E_SCORE = 2.072, 1.302, 2.43
class TestBarnaba(unittest.TestCase):
    def test_rmsd(self):
        rmsd = ScoreBarnaba.compute_rmsd(STRUCT1, STRUCT2)
        self.assertEqual(rmsd, RMSD)

    def test_ermsd(self):
        e_rmsd = ScoreBarnaba.compute_ermsd(STRUCT1, STRUCT2)
        self.assertEqual(e_rmsd, E_RMSD)

    def test_escore(self):
        e_score = ScoreBarnaba.compute_escore(STRUCT1, STRUCT2)
        self.assertEqual(e_score, E_SCORE)
