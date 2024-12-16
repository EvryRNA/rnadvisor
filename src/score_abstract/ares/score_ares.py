"""
Class that implements the ARES score.

Original code from:
https://zenodo.org/records/5090151/files/e3nn_ares.zip
and
https://zenodo.org/records/6893040/files/ares_release.zip

I used the installation processes from the dockerhub of "adamczykb/ares_qa"

Original paper:
Raphael J. L. Townshend et al. ,
Geometric deep learning of RNA structure.
Science373,1047-1051(2021).
DOI:10.1126/science.abe5650
"""

import os
from typing import Dict, List, Optional, Tuple
from src.score_abstract.score_abstract import ScoreAbstract
from src.utils import time_it
import shutil
from typing import Dict, Optional, Tuple
import os
import torch_geometric
import atom3d.datasets as da
import lib.ares.ares_release.ares.data as d
import lib.ares.ares_release.ares.model as m
import pytorch_lightning as pl
import logging
import warnings

logging.getLogger("torch").setLevel(logging.ERROR)
logging.getLogger("lightning").setLevel(logging.ERROR)
warnings.filterwarnings(
    "ignore", category=UserWarning, module="pytorch_lightning.utilities.distributed"
)


class ScoreARES(ScoreAbstract):
    """
    Class that implements the ARES code.
    """

    def __init__(self, ares_weights: Optional[str] = None, *args, **kwargs):
        super(ScoreARES, self).__init__(*args, **kwargs)
        self.ares_weights = (
            ares_weights
            if ares_weights is not None
            else os.path.join("lib", "ares", "ares_release", "data", "weights.ckpt")
        )

    @staticmethod
    def compute_ares(pred_path: str, ares_weights: Optional[str] = None) -> List:
        """
        Compute the ARES scoring function.
        :param pred_path: path to a .pdb file
        :return: the ARES score
        """
        return round(ScoreARES(ares_weights).predict_model(pred_path), 3)

    def predict_model(self, pred_path: str):
        """Load the ARES model and create the dataset, trainer."""
        tmp_dir = os.path.join("tmp", "ares")
        os.makedirs(tmp_dir, exist_ok=True)
        shutil.copy(pred_path, tmp_dir)
        transform = d.create_transform(False, None, "pdb")
        dataset = da.load_dataset(tmp_dir, "pdb", transform)
        dataloader = torch_geometric.data.DataLoader(dataset, batch_size=1, num_workers=0)
        tfnn = m.ARESModel.load_from_checkpoint(self.ares_weights)
        trainer = pl.Trainer(progress_bar_refresh_rate=0, logger=False)
        out = trainer.test(tfnn, dataloader, verbose=False)
        return out[0]["test_loss"]

    @time_it
    def _compute(self, pred_path: str, native_path: str, *args, **kwargs) -> Tuple[Dict, Dict]:
        ares = self.compute_ares(pred_path, self.ares_weights)
        return {"ARES": ares}  # type: ignore
