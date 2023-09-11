"""Class that does the unit tests for the rna tools code."""
import os
import unittest

from src.score_abstract.score_rna_assessment.score_di import ScoreDI
from src.score_abstract.score_rna_assessment.score_inf import ScoreINF
from src.score_abstract.score_rna_assessment.score_p_value import ScorePValue
from src.score_abstract.score_rna_assessment.score_rmsd import ScoreRMSD

STRUCT1 = os.path.join("tests", "data", "structure_1.pdb")
STRUCT2 = os.path.join("tests", "data", "structure_2.pdb")

TRUE_SCORES = {
    "RMSD": 20.162562637460915,
    "P-VALUE": 4.9005046132144514e-08,
    "INF-ALL": 0.7927294447919914,
    "INF-WC": 0.8948381385019567,
    "INF-NWC": 0.31622776601683794,
    "INF-STACK": 0.7867155194709718,
    "DI": 25.43435565554334
}

class TestRNAAssessmentScore(unittest.TestCase):
    """Unit tests for the RMSD, p-value, INF and DI."""

    def test_rmsd(self):
        rmsd_pred = ScoreRMSD.compute_rmsd(STRUCT1, STRUCT2)
        rmsd_pred_self_1 = ScoreRMSD.compute_rmsd(STRUCT1, STRUCT1)
        rmsd_pred_self_2 = ScoreRMSD.compute_rmsd(STRUCT2, STRUCT2)
        self.assertAlmostEqual(rmsd_pred, TRUE_SCORES['RMSD'])
        self.assertAlmostEqual(rmsd_pred_self_1, 0)
        self.assertAlmostEqual(rmsd_pred_self_2, 0)


    def test_p_value(self):
        p_value_pred = ScorePValue.compute_p_value(STRUCT1, STRUCT2)
        self.assertAlmostEqual(p_value_pred, TRUE_SCORES['P-VALUE'])

    def test_inf_all(self):
        inf_all_pred = ScoreINF.compute_inf_all(STRUCT1, STRUCT2)
        self_score_1 = ScoreINF.compute_inf_all(STRUCT1, STRUCT1)
        self_score_2 = ScoreINF.compute_inf_all(STRUCT2, STRUCT2)
        self.assertAlmostEqual(inf_all_pred, TRUE_SCORES['INF-ALL'])
        self.assertAlmostEqual(self_score_1, 1)
        self.assertAlmostEqual(self_score_2, 1)

    def test_inf_wc(self):
        inf_wc_pred = ScoreINF.compute_inf_wc(STRUCT1, STRUCT2)
        self_score_1 = ScoreINF.compute_inf_wc(STRUCT1, STRUCT1)
        self_score_2 = ScoreINF.compute_inf_wc(STRUCT2, STRUCT2)
        self.assertAlmostEqual(inf_wc_pred, TRUE_SCORES['INF-WC'])
        self.assertAlmostEqual(self_score_1, 1)
        self.assertAlmostEqual(self_score_2, 1)

    def test_inf_nwc(self):
        inf_nwc_pred = ScoreINF.compute_inf_nwc(STRUCT1, STRUCT2)
        self_score_1 = ScoreINF.compute_inf_nwc(STRUCT1, STRUCT1)
        self_score_2 = ScoreINF.compute_inf_nwc(STRUCT2, STRUCT2)
        self.assertAlmostEqual(inf_nwc_pred, TRUE_SCORES['INF-NWC'])
        self.assertAlmostEqual(self_score_1, 1)
        self.assertAlmostEqual(self_score_2, 1)

    def test_inf_stack(self):
        inf_stack_pred = ScoreINF.compute_inf_stack(STRUCT1, STRUCT2)
        self_score_1 = ScoreINF.compute_inf_stack(STRUCT1, STRUCT1)
        self_score_2 = ScoreINF.compute_inf_stack(STRUCT2, STRUCT2)
        self.assertAlmostEqual(inf_stack_pred, TRUE_SCORES['INF-STACK'])
        self.assertAlmostEqual(self_score_1, 1)
        self.assertAlmostEqual(self_score_2, 1)

    def test_di(self):
        di_pred = ScoreDI.compute_di(STRUCT1, STRUCT2)
        self_score_1 = ScoreDI.compute_di(STRUCT1, STRUCT1)
        self_score_2 = ScoreDI.compute_di(STRUCT2, STRUCT2)
        self.assertAlmostEqual(di_pred, TRUE_SCORES['DI'])
        self.assertAlmostEqual(self_score_1, 0)
        self.assertAlmostEqual(self_score_2, 0)
