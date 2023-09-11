"""
File that converts the string name of scoring methods to the appropriate class
"""
from typing import Dict

from src.score_abstract.barnaba.score_barnaba import ScoreBarnaba
from src.score_abstract.dfire.score_dfire import ScoreDfire
from src.score_abstract.mcq4structures.score_mcq import ScoreMCQ
from src.score_abstract.rasp.score_rasp import ScoreRASP
from src.score_abstract.rs_rnasp.score_rs_rnasp import ScoreRsRNASP
from src.score_abstract.score_rna_assessment.score_clash import ScoreClash
from src.score_abstract.score_rna_assessment.score_di import ScoreDI
from src.score_abstract.score_rna_assessment.score_inf import ScoreINF
from src.score_abstract.score_rna_assessment.score_p_value import ScorePValue
from src.score_abstract.score_rna_assessment.score_rmsd import ScoreRMSD
from src.score_abstract.score_voronota.score_cad import ScoreCAD
from src.score_abstract.score_zhanggroup.tm_gdt_scores import TmGdtScores

CONVERT_NAME_TO_SCORING_CLASS: Dict = {
    "RMSD": ScoreRMSD,
    "P-VALUE": ScorePValue,
    "INF": ScoreINF,
    "DI": ScoreDI,
    "MCQ": ScoreMCQ,
    "TM-SCORE": TmGdtScores,
    "CAD": ScoreCAD,
    "RASP": ScoreRASP,
    "CLASH": ScoreClash,
    "BARNABA": ScoreBarnaba,
    "DFIRE": ScoreDfire,
    "rsRNASP": ScoreRsRNASP,
}
