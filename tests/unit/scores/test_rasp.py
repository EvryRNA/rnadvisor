"""Class that implements the test for the RASP scores."""
import os
import unittest

from src.score_abstract.rasp.score_rasp import ScoreRASP

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

TRUE_RASP1 = [-51431.1, 586410.0, -0.0877051]
TRUE_RASP2 = [-61642.1, 484584.0, -0.127206]
class TestRASP(unittest.TestCase):
    def test_rasp(self):
        rasp1 = ScoreRASP.compute_rasp(STRUCT1)
        rasp2 = ScoreRASP.compute_rasp(STRUCT2)
        self.assertAlmostEqual(rasp1, TRUE_RASP1)
        self.assertAlmostEqual(rasp2, TRUE_RASP2)
