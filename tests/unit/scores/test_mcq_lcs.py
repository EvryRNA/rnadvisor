"""Class that tests the LCS-TA code"""
import os
import unittest

from src.score_abstract.mcq4structures.score_mcq_lcs import ScoreMCQLCS

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

TRUE_LCS_COV, TRUE_LCS_RESIDUE = 100, 101


class TestMCQLCS(unittest.TestCase):
    def test_mcq_lcs(self):
        coverage, residues = ScoreMCQLCS.compute_mcq_lcs(STRUCT1, STRUCT2)
        self.assertEqual(coverage, TRUE_LCS_COV)
        self.assertEqual(residues, TRUE_LCS_RESIDUE)

