"""Class that implements the test for the cgRNASP score."""
import os
import unittest

from src.score_abstract.cgrnasp.score_cgrnasp import ScoreCGRNASP

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

cgRNASP_1, cgRNASP_2 = -838.738, -738.173
cgRNASP_C_1, cgRNASP_C_2 = -1554.473, -1501.9
cgRNASP_PC_1, cgRNASP_PC_2 = -431.953, -410.667


class TestARES(unittest.TestCase):
    def test_cgrnasp(self):
        cgrnasp_1 = ScoreCGRNASP.compute_cgrnasp(STRUCT1)
        cgrnasp_2 = ScoreCGRNASP.compute_cgrnasp(STRUCT2)
        print(cgrnasp_1, cgrnasp_2)
        self.assertEqual(cgrnasp_1, cgRNASP_1)
        self.assertEqual(cgrnasp_2, cgRNASP_2)

    def test_cgrnasp_c(self):
        cgrnasp_1 = ScoreCGRNASP.compute_cgrnasp_c(STRUCT1)
        cgrnasp_2 = ScoreCGRNASP.compute_cgrnasp_c(STRUCT2)
        print(cgrnasp_1, cgrnasp_2)
        self.assertEqual(cgrnasp_1, cgRNASP_C_1)
        self.assertEqual(cgrnasp_2, cgRNASP_C_2)

    def test_cgrnasp_pc(self):
        cgrnasp_1 = ScoreCGRNASP.compute_cgrnasp_pc(STRUCT1)
        cgrnasp_2 = ScoreCGRNASP.compute_cgrnasp_pc(STRUCT2)
        print(cgrnasp_1, cgrnasp_2)
        self.assertEqual(cgrnasp_1, cgRNASP_PC_1)
        self.assertEqual(cgrnasp_2, cgRNASP_PC_2)
