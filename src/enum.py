"""
File that converts the string name of scoring methods to the appropriate class
"""

from typing import Dict

from src.score_abstract.barnaba.score_barnaba import ScoreBarnaba
from src.score_abstract.dfire.score_dfire import ScoreDfire
from src.score_abstract.mcq4structures.score_mcq import ScoreMCQ
from src.score_abstract.openstructure.qs_score import QSScore
from src.score_abstract.openstructure.score_lddt import ScorelDDT
from src.score_abstract.openstructure.tm_score import TMScore
from src.score_abstract.rasp.score_rasp import ScoreRASP
from src.score_abstract.rs_rnasp.score_rs_rnasp import ScoreRsRNASP
from src.score_abstract.score_rna_assessment.score_clash import ScoreClash
from src.score_abstract.score_rna_assessment.score_di import ScoreDI
from src.score_abstract.score_rna_assessment.score_inf import ScoreINF
from src.score_abstract.score_rna_assessment.score_p_value import ScorePValue
from src.score_abstract.score_rna_assessment.score_rmsd import ScoreRMSD
from src.score_abstract.score_voronota.score_cad import ScoreCAD
from src.score_abstract.score_zhanggroup.tm_gdt_scores import GdtScores
from src.score_abstract.mcq4structures.score_mcq_lcs import ScoreMCQLCS
from src.score_abstract.cgrnasp.score_cgrnasp import ScoreCGRNASP
from src.score_abstract.tb_mcq.score_tb_mcq import ScoreTBMCQ
from src.score_abstract.score_zhanggroup.tm_score_us import TMScoreUS

CONVERT_NAME_TO_SCORING_CLASS: Dict = {
    "RMSD": ScoreRMSD,
    "P-VALUE": ScorePValue,
    "INF": ScoreINF,
    "DI": ScoreDI,
    "MCQ": ScoreMCQ,
    "GDT-TS": GdtScores,
    "CAD": ScoreCAD,
    "RASP": ScoreRASP,
    "CLASH": ScoreClash,
    "BARNABA": ScoreBarnaba,
    "DFIRE": ScoreDfire,
    "rsRNASP": ScoreRsRNASP,
    "lDDT": ScorelDDT,
    "TM-SCORE (OST)": TMScore,
    "TM-SCORE": TMScoreUS,
    "QS-SCORE": QSScore,
    "LCS-TA": ScoreMCQLCS,
    "CGRNASP": ScoreCGRNASP,
    "TB-MCQ": ScoreTBMCQ,
}
LIST_ALL_METRICS = [
    "RMSD",
    "P-VALUE",
    "INF",
    "DI",
    "MCQ",
    "TM-SCORE",
    "CAD",
    "BARNABA",
    "CLASH",
    "GDT-TS",
    "lDDT",
    "QS-SCORE",
    "LCS-TA",
]
LIST_ALL_ENERGIES = ["BARNABA", "DFIRE", "rsRNASP", "RASP", "CGRNASP", "TB-MCQ"]
DECOYS_LIMITED = ["DFIRE", "BARNABA"]
DISTINCT_METRICS = ["DI", "GDT-TS", "MCQ"]
