from src.score_abstract.score_abstract import ScoreAbstract
from src.score_abstract.tb_mcq.helper.extractor_helper import ExtractorHelper
from src.score_abstract.tb_mcq.helper.rna_torsionbert_helper import RNATorsionBERTHelper
from src.score_abstract.tb_mcq.metrics.mcq import MCQ
from typing import Dict, Tuple
from src.utils import time_it


class ScoreTBMCQ(ScoreAbstract):
    def __init__(self, *args, **kwargs):
        super(ScoreTBMCQ, self).__init__(*args, **kwargs)

    @time_it
    def _compute(self, pred_path: str, native_path: str, *args, **kwargs) -> Tuple[Dict, Dict]:
        """
        Compute the TB-MCQ: MCQ between predicted angles from RNA-TorsionBERT and inferred angles
        from the structure
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return:
        """
        tb_mcq = self.compute_tb_mcq(pred_path)
        return {"TB-MCQ": tb_mcq}

    def compute_tb_mcq(self, pred_path: str) -> float:
        """
        Compute the TB-MCQ with RNA-TorsionBERT model
        :param pred_path: the path to the .pdb file of a prediction.
                It could be a native or a predicted structure.
        """
        experimental_angles = ExtractorHelper().extract_all(pred_path)
        sequence = "".join(experimental_angles["sequence"].values)
        torsionBERT_helper = RNATorsionBERTHelper()
        torsionBERT_output = torsionBERT_helper.predict(sequence)
        mcq = MCQ().compute_mcq(experimental_angles, torsionBERT_output)
        return mcq
