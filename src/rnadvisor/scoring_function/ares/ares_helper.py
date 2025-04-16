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

from typing import List
import shutil
from typing import Dict, Optional, Tuple
import os
import numpy as np
import torch_geometric
import atom3d.datasets as da
import lib.ares.ares_release.ares.data as d
import lib.ares.ares_release.ares.model as m
import pytorch_lightning as pl
import logging
from tqdm import tqdm
import warnings
from loguru import logger

logging.getLogger("torch").setLevel(logging.ERROR)
logging.getLogger("lightning").setLevel(logging.ERROR)
warnings.filterwarnings(
    "ignore", category=UserWarning, module="pytorch_lightning.utilities.distributed"
)

from rnadvisor.utils.utils import time_it
from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract

REDUCE_COMMAND = "reduce -NOFLIP $INPUT_PATH > $OUTPUT_PATH 2>/dev/null"

class AresHelper(PredictAbstract):
    """
    Class that implements the ARES code.
    """

    def __init__(self, ares_weights: Optional[str] = None, *args, **kwargs):
        super(AresHelper, self).__init__(name="ares",*args, **kwargs)
        self.ares_weights = (
            ares_weights
            if ares_weights is not None
            else os.path.join("lib", "ares", "ares_release", "data", "weights.ckpt")
        )
        self.tmp_dir = os.path.join("tmp", "ares", "inputs")
        os.makedirs(self.tmp_dir, exist_ok=True)

    def compute_ares(self, pred_path: str, ares_weights: Optional[str] = None) -> List:
        """
        Compute the ARES scoring function.
        :param pred_path: path to a .pdb file
        :return: the ARES score
        """
        return round(self.predict_model(pred_path), 3)

    def reduce_data(self, pred_paths: List[str]):
        """
        Add Hydrogren molecules. Needed for ARES to run.
        Word, et. al. (1999) J. Mol. Biol. 285, 1735-1747.
        :param pred_paths: list of input paths
        """
        logger.debug("Reducing data for ARES scoring function.")
        for pred_path in tqdm(pred_paths):
            out_path = os.path.join(self.tmp_dir, os.path.basename(pred_path))
            command = REDUCE_COMMAND.replace("$INPUT_PATH", pred_path).replace("$OUTPUT_PATH", out_path)
            if not os.path.exists(out_path):
                os.system(command)
        logger.debug("Data reduced for ARES scoring function.")
        logger.debug("Starting ARES prediction.")


    def prepare_data(self, native_path: Optional[str], pred_paths: List[str], *args, **kwargs):
        """
        Prepare the data for the metric/scoring function.
        It can be the load of the model or the preprocessing of the data.
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_paths: list of paths to RNA `.pdb` files.
        """
        self.tfnn = m.ARESModel.load_from_checkpoint(self.ares_weights)
        self.trainer = pl.Trainer(progress_bar_refresh_rate=0, logger=False)
        self.reduce_data(pred_paths)

    def predict_model(self, pred_path: str):
        """Load the ARES model and create the dataset, trainer."""
        rna_name = os.path.basename(pred_path)
        tmp_dir = os.path.join("tmp", "ares", "dataset")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        os.makedirs(tmp_dir, exist_ok=True)
        in_path = os.path.join(self.tmp_dir, rna_name)
        shutil.copy(in_path, tmp_dir)
        transform = d.create_transform(False, None, "pdb")
        dataset = da.load_dataset(tmp_dir, "pdb", transform)
        dataloader = torch_geometric.data.DataLoader(dataset, batch_size=1, num_workers=1)
        try:
            out = self.trainer.test(self.tfnn, dataloader, verbose=False)
        except (RuntimeError, KeyError):
            # Even with reduce, the prediction was not successful
            return np.nan
        return out[0]["test_loss"]

    @time_it
    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        ares = self.compute_ares(pred_path, self.ares_weights)
        return {"ARES": ares}  # type: ignore

main = build_predict_cli(AresHelper)

if __name__ == "__main__":
    main()
