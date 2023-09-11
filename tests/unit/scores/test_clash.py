"""Class to test the clash score"""
import os
import unittest

from src.score_abstract.score_rna_assessment.score_clash import ScoreClash

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")
STRUCT3 = os.path.join("tests", "data", "structure_clash.pdb")

CLASH1, CLASH2, CLASH3 = 0, 0, 0.726
class TestClashScore(unittest.TestCase):
    def test_clash_score(self):
        clash1 = ScoreClash.compute_clash_score(STRUCT1)
        clash2 = ScoreClash.compute_clash_score(STRUCT2)
        clash3 = ScoreClash.compute_clash_score(STRUCT3)

        self.assertAlmostEqual(clash1, CLASH1)
        self.assertAlmostEqual(clash2, CLASH2)
        self.assertAlmostEqual(clash3, CLASH3)