"""
Class that runs the PAMNet score.
The original github code is the following:
    https://github.com/XieResearchGroup/Physics-aware-Multiplex-GNN
The original paper is:
Zhang, S., Liu, Y. & Xie, L.
A universal framework for accurate and efficient geometric deep learning of molecular systems.
Sci Rep 13, 19171 (2023).
https://doi.org/10.1038/s41598-023-46382-8
"""
import os
import shutil
from typing import Optional, List

import torch
import time
import pandas as pd

from rnadvisor.predict_abstract import PredictAbstract

from rnadvisor.cli_runner import build_predict_cli

from loguru import logger
import sys


sys.path.append('pamnet')
from models import PAMNet, Config
from inference_rna_puzzles import predict
from preprocess_rna_puzzles import construct_graphs
import tempfile

class PAMNetHelper(PredictAbstract):
    def __init__(self,  *args, **kwargs):
        super().__init__(name="PAMNet", *args, **kwargs)
        self.tmp_dir = tempfile.mkdtemp(prefix="pamnet")
        self.model = self.get_model()

    @staticmethod
    def get_model():
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if torch.cuda.is_available():
            torch.cuda.set_device(0)
        config = Config(dataset="rna_native", dim=16, n_layer=1,
                        cutoff_l=2.6,
                        cutoff_g=20.0, flow="target_to_source")

        model = PAMNet(config).to(device)
        model.load_state_dict(torch.load("pamnet/save/" + "pamnet_rna.pt", map_location=device))
        model.eval()
        return model

    def preprocess(self, in_dir: str):
        """
        Construct the graph processing by PAMNet
        """
        os.makedirs(self.tmp_dir, exist_ok=True)
        construct_graphs(in_dir, self.tmp_dir, "rna_graphs")

    def prepare_data(self, native_path: Optional[str], pred_paths: List[str], *args, **kwargs):
        """
        Prepare the data for the metric/scoring function.
        It can be the load of the model or the preprocessing of the data.
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_paths: list of paths to RNA `.pdb` files.
        """
        pass

    def predict_dir(self, native_path: Optional[str], pred_dir: Optional[str], out_path: Optional[str],
                    out_time_path: Optional[str], *args, **kwargs):
        """
        Compute the metric/scoring function for a given directory/path.
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_dir: path to a directory or single RNA `.pdb` file.
        :param out_path: path to a `.csv` file where to save the predictions.
        :param out_time_path: path to a `.csv` file where to save the time taken for each prediction.
        """
        native_path, pred_paths, out_path, out_time_path = self._init_dir_preds(native_path, pred_dir, out_path, out_time_path)
        self.prepare_data(native_path, pred_paths, *args, **kwargs)
        self.preprocess(pred_dir)
        in_path, dataset = self.tmp_dir, "rna_graphs"
        time_b = time.time()
        df = predict(in_path, dataset, 1, None, self.model)
        time_all = time.time() - time_b
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        scores = df.rename_axis("rna")
        times = pd.DataFrame({"rna": list(scores.index), self.name: [time_all/len(df)]*len(df)})
        logger.info(f"Saving predictions to {out_path}")
        scores.to_csv(out_path, index=True)
        logger.info(f"Saving time to {out_time_path}")
        times.to_csv(out_time_path, index=False)

main = build_predict_cli(PAMNetHelper)

if __name__ == "__main__":
    main()