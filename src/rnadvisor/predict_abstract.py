import os
import sys

from loguru import logger
from typing import Optional, Tuple, List, Dict

from tqdm import tqdm
import pandas as pd

from rnadvisor.utils.utils import time_it



class PredictAbstract:
    def __init__(self, name: str, quiet: bool = False, *args, **kwargs):
        """
        Name of the given metric/scoring function
        :param name: name to be saved in the final csv
        """
        self.name = name
        self.kwargs = kwargs
        if quiet:
            logger.remove()
            logger.add(sys.stderr, level="WARNING")

    def init_paths(self, native_path: Optional[str], pred_dir: Optional[str]) -> Tuple[Optional[str], List[str]]:
        """
        Initialise the different paths depending if there is a native path or not
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_dir: path to a directory or single RNA `.pdb` file.
        :return: the native path (or None) and the list of RNA paths
        """
        if native_path is None and pred_dir is None:
            msg = "Either native_path or pred_dir must be provided."
            logger.error(msg)
            raise ValueError(msg)
        elif native_path is not None and pred_dir is None:
            logger.info(f"No prediction directory provided. Using native path: {native_path}")
            return native_path, [native_path]
        elif native_path is not None and pred_dir is not None:
            if os.path.isdir(pred_dir):
                pred_paths = [os.path.join(pred_dir, f) for f in os.listdir(pred_dir) if f.endswith(".pdb")]
            elif os.path.isfile(pred_dir):
                pred_paths = [pred_dir]
            else:
                msg = f"Prediction directory {pred_dir} is not a valid file or directory. You might " \
                      f"want to use docker volume to ensure this path is valid inside the container."
                logger.error(msg)
                raise ValueError(msg)
            logger.info(f"Using native path: {native_path} and prediction directory: {pred_dir}")
            logger.info(f"Found {len(pred_paths)} RNA files in prediction directory.")
            return native_path, pred_paths
        elif native_path is None and pred_dir is not None:
            if os.path.isdir(pred_dir):
                pred_paths = [os.path.join(pred_dir, f) for f in os.listdir(pred_dir) if f.endswith(".pdb")]
            elif os.path.isfile(pred_dir):
                pred_paths = [pred_dir]
            else:
                msg = f"Prediction directory {pred_dir} is not a valid file or directory."
                logger.error(msg)
                raise ValueError(msg)

            logger.info(f"Using prediction directory: {pred_dir}")
            logger.info(f"Found {len(pred_paths)} RNA files in prediction directory.")
            return None, pred_paths

    def prepare_data(self, native_path: Optional[str], pred_paths: List[str], *args, **kwargs):
        """
        Prepare the data for the metric/scoring function.
        It can be the load of the model or the preprocessing of the data.
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_paths: list of paths to RNA `.pdb` files.
        """
        pass

    def _init_dir_preds(self, native_path: Optional[str], pred_dir: Optional[str],
                        out_path: Optional[str], out_time_path: Optional[str]) -> Tuple[Optional[str], List[str], Optional[str],
    Optional[str]]:
        """
        Initialise the different paths for the predictions
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_dir: path to a directory or single RNA `.pdb` file.
        :param out_path: path to a `.csv` file where to save the predictions.
        :param out_time_path: path to a `.csv` file where to save the time taken for each prediction.
        :return:
        """
        native_path, pred_paths = self.init_paths(native_path, pred_dir)
        out_path, out_time_path = self.init_out_path(out_path, out_time_path)
        return native_path, pred_paths, out_path, out_time_path

    @staticmethod
    def init_out_path(out_path: Optional[str], out_time_path: Optional[str]) -> Tuple[str, str]:
        """
        Initialise the output paths for the predictions.
        Create necessary directories if needed.
        :param out_path: path to a .csv file where to save the predictions.
        :param out_time_path: path to a .csv file where to save the time taken for each prediction.
        """
        if out_path is None:
            out_path = os.path.join("data", "rnadvisor_output.csv")
            os.makedirs("data", exist_ok=True)
            logger.warning(f"No output path provided. Predictions will be saved in {out_path}")
        else:
            dir_name = os.path.dirname(out_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
        if out_time_path is None:
            logger.warning(f"No output time path provided. Time will not be saved")
        else:
            dir_name = os.path.dirname(out_time_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
        return out_path, out_time_path

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
        scores: Dict = {"rna": []}
        times: Dict = {"rna": []}
        self.prepare_data(native_path, pred_paths, *args, **kwargs)
        with tqdm(pred_paths, desc="Predicting") as pbar:
            for pred_path in pbar:
                c_scores, c_times = self.predict_single_file(native_path, pred_path, *args, **kwargs, **self.kwargs)
                for score_n, score in c_scores.items():
                    scores[score_n] = scores.get(score_n, []) + [score]
                    times[score_n] = times.get(score_n, []) + [c_times[score_n]]
                rna_name = os.path.basename(pred_path)
                scores["rna"].append(rna_name)
                times["rna"].append(rna_name)
                short_path = os.path.basename(pred_path)
                score_key, score_val = list(c_scores.items())[ 0]
                pbar.set_postfix({"file": short_path, score_key: f"{score_val:.4f}"})
        self.save_df(scores, times, out_path, out_time_path)

    def save_df(self, scores: Dict, times: Dict, out_path: Optional[str], out_time_path: Optional[str]):
        """
        Save the output dictionary into dataframes
        :param scores: predicted scores
        :param times: time for each RNA
        :param out_path: path where to save the predictions
        :param out_time_path: path where to save the times for each prediction
        """
        scores_df = pd.DataFrame(scores)
        times_df = pd.DataFrame(times)
        logger.info(f"Saving predictions to {out_path}")
        scores_df.to_csv(out_path, index=False, float_format="%.3f")
        logger.info(f"Saving time to {out_time_path}")
        times_df.to_csv(out_time_path, index=False, float_format="%.3f")
        logger.info(f"Results: \n{scores_df}")

    @time_it
    def predict_single_file(self, native_path: Optional[str], pred_path: str, *args, **kwargs) -> Dict:
        raise NotImplementedError("This method should be implemented in the child class")