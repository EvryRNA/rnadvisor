"""File to test the Voronota implementation of the CAD score"""
import os
import unittest

from src.score_abstract.score_voronota.score_cad import ScoreCAD

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

TRUE_CAD_SCORE_1_2 = 0.814618
TRUE_CAD_SCORE_2_1 = 0.766022

class TestVoronota(unittest.TestCase):
    """Unit tests for CAD score"""
    def test_cad_score(self):
        cad_score = ScoreCAD.compute_cad_score(STRUCT1, STRUCT2)
        cad_score_2 = ScoreCAD.compute_cad_score(STRUCT2, STRUCT1)
        self.assertAlmostEqual(TRUE_CAD_SCORE_1_2, cad_score)
        self.assertAlmostEqual(TRUE_CAD_SCORE_2_1, cad_score_2)
