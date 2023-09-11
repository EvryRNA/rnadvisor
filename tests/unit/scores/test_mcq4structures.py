"""Class that tests the MCQ4Structures code for the MCQ score"""
import os
import unittest

from src.score_abstract.mcq4structures.score_mcq import ScoreMCQ

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

TRUE_MCQ = 32.51

class TestMCQ4Structures(unittest.TestCase):
    def test_mcq(self):
        score = ScoreMCQ.compute_mcq(STRUCT1, STRUCT2)
        self.assertAlmostEqual(TRUE_MCQ, score)

