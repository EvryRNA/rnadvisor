"""Class that convert the scoring class to command line. It predicts the scores from .pdb files."""
import argparse
import os.path
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from lib.rna_assessment.RNA_normalizer.structures.pdb_normalizer import PDBNormalizer
from loguru import logger
from tqdm import tqdm

from src.enum import CONVERT_NAME_TO_SCORING_CLASS, LIST_ALL_METRICS, LIST_ALL_ENERGIES
from src.score_abstract.score_abstract import ScoreAbstract
from src.utils import read_yaml_to_dict


class RNAdvisorCLI:
    def __init__(
        self,
        pred_path: str,
        native_path: str,
        result_path: Optional[str] = "results",
        all_scores: Optional[List[ScoreAbstract]] = None,
        normalise: bool = True,
        sort_by: Optional[str] = "RMSD",
        time_path: Optional[str] = None,
        verbose: bool = False,
        log_path: Optional[str] = "out.log",
        *args,
        **kwargs,
    ):
        """
        Initialise the scoring class.
        :param pred_path: directory to .pdb files or path to a .pdb file of the predictions.
        :param native_path: path to a .pdb file of the native structure.
        :param result_path: path to a directory or a file where to store the different scores.
        :param all_scores: a list of instances of ScoreAbstract. These are the scores that will be
                computed.
        :param normalise: whether to normalise the structures or not
        :param sort_by: by which score do we sort the outputs
        :param time_path: path to a file where to store the time taken to compute the scores
        :param verbose: whether to print the logs or not
        :param log_path: path where are stored the different logs
        """
        self._init_logger(verbose, log_path)
        self.normalise = normalise
        self.pred_path, self.model_name = self._init_pred_path(pred_path)
        self.native_path = self._init_native_path(native_path)
        self.result_path = self._init_result_path(result_path)
        self.all_scores = self.init_scores(all_scores)
        self.sort_by = sort_by
        self.time_path = time_path
        self.log_path = log_path

    def _init_logger(self, verbose: bool, log_path: Optional[str]):
        """
        Initialise the logger parameters.
        :param verbose: whether to print the debug logs in terminal
        :param log_path: path where to save the log files.
        """
        logger.remove()
        logger.add(sys.stderr, level="DEBUG" if verbose else "INFO")
        if log_path is not None:
            dir_name = os.path.dirname(log_path)
            if dir_name != "":
                os.makedirs(dir_name, exist_ok=True)
            logger.add(log_path, level="DEBUG", mode="w")

    def _normalise(self, input_path: Union[List[str], str]):
        """
        Normalise the file or list of files.
        :param input_path: a path to a .pdb file or list of paths
        :return: new paths with the normalized structures
        """
        dirname = os.path.join("tmp", "inputs")
        os.makedirs(dirname, exist_ok=True)
        if type(input_path) is str:
            new_path = os.path.join(dirname, "normalized_" + os.path.basename(input_path))
            output = self.normalize_structure(input_path, new_path)
            new_path = new_path if output else input_path
            return new_path
        else:
            new_paths = []
            for path in input_path:
                new_path = self._normalise(path)
                new_paths.append(new_path)
            return new_paths

    @staticmethod
    def init_scores(
        all_scores: Optional[List[ScoreAbstract]] = None,
    ) -> List[ScoreAbstract]:
        """
        Initialise the different scores to the associated classes that implement the 'compute'
                function
        :param all_scores: a list of instances of ScoreAbstract. These are the scores that will be
                computed. If None, it will load the scores from the config.py file
        :return: a dictionary with the name of the score, and the instantiated class
        """
        if all_scores is None:
            raise NotImplementedError("NO SCORES TO OUTPUT")
        return all_scores

    def _init_result_path(self, result_path: Optional[str]) -> Optional[str]:
        """
        Initialise the path where to store the results.
        :param result_path: path to a directory. It can exist or not.
        :return: the path to a directory that has been created.
        """
        if result_path is None:
            return None
        if os.path.isfile(result_path):
            # Path to an existing path
            error_msg = "PATH TO THE LOG ALREADY EXIST AND IS A FILE. IT WILL OVERWRITE IT."
            logger.debug(error_msg)
        elif result_path.endswith(".csv"):
            # Save a .csv file. Need to check if the path exists
            dir_path = os.path.dirname(result_path)
            os.makedirs(dir_path, exist_ok=True)
        else:
            # Otherwise, create the path. Do nothing if the directory already existed.
            os.makedirs(result_path, exist_ok=True)
            # Get datetime to store the result with the datetime.
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H:%M:%S")
            result_path = os.path.join(result_path, "scores_" + dt_string + ".csv")
        return result_path

    def _init_native_path(self, native_path: str) -> str:
        """
        Initialise the path for the native .pdb structure
        :param native_path: a path to a .pdb native structure
        :return: the path if it exists and is a .pdb
        """
        error_msg = None
        if not os.path.exists(native_path):
            # The path doesn't exist
            error_msg = "NATIVE PATH DOESN'T EXIST"
        if not native_path.endswith(".pdb"):
            # The path isn't a .pdb file
            error_msg = "NATIVE PATH ISN'T A .pdb FILE"
        if error_msg is not None:
            # Show the error
            logger.debug(error_msg)
            raise FileNotFoundError(error_msg)
        if self.normalise:
            return self._normalise(native_path)
        return native_path

    def _init_pred_path(self, pred_path: str) -> Tuple[List[str], str]:
        """
        Initialise the path for the different predictions.
        It returns a list of paths of the different predictions, and the name of the model.
        If the pred_path is a path to a .pdb file (and not a directory of .pdb files), the list
        has one element
        The name of the model is either the last name of the directory, or the path.
        :param pred_path: directory to .pdb files or path to a .pdb file
        :return: a list of the different .pdb files and the name of the model.
        """
        paths, model_name = [], ""
        if not os.path.exists(pred_path):
            # Path doesn't exist
            error_msg = "PREDICTION PATH DOESN'T EXIST"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        if os.path.isdir(pred_path):
            # Directory of .pdb files
            paths = os.listdir(pred_path)
            model_name = os.path.basename(pred_path)
            # Filter the pdb files and add full path
            paths = [
                os.path.join(pred_path, c_path) for c_path in paths if c_path.endswith(".pdb")
            ]
        elif os.path.isfile(pred_path):
            # Path to one .pdb file
            if not pred_path.endswith(".pdb"):
                error_msg = "PREDICTION PATH ISN'T .pdb FILE"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)
            model_name = pred_path
            paths = [pred_path]
        if self.normalise:
            return self._normalise(paths), model_name
        return paths, model_name

    @staticmethod
    def get_arguments():
        """Function to get arguments from command line. Otherwise, load it from config file."""
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument(
            "--pred_path",
            dest="pred_path",
            type=str,
            help="Directory to .pdb files or path to a .pdb file of the predictions.",
        )
        parser.add_argument(
            "--native_path",
            dest="native_path",
            type=str,
            help="Path to a .pdb file of the native structure.",
        )
        parser.add_argument(
            "--result_path",
            dest="result_path",
            type=str,
            help="Path to a directory where to store the different scores.",
        )
        parser.add_argument(
            "--all_scores",
            dest="all_scores",
            default="RMSD,P-VALUE,INF,DI,MCQ,TM-SCORE,CAD",
            type=str,
            help="List of the scores to use, separated by a comma. "
            "If you want to use them all, use ALL. "
            "Choice between RMSD,P-VALUE,INF,DI,MCQ,TM-SCORE,CAD.",
        )
        parser.add_argument(
            "--no_normalisation",
            dest="normalise",
            action="store_false",
            default=True,
            help="If you want to remove the normalisation process on the .pdb files.",
        )
        parser.add_argument(
            "--config_path",
            dest="config_path",
            default=None,
            type=str,
            help="Path to the config.yaml file with the different parameters.",
        )
        parser.add_argument(
            "--sort_by",
            dest="sort_by",
            default="RMSD",
            type=str,
            help="Which score to sort the results by",
        )
        parser.add_argument(
            "--time_path",
            dest="time_path",
            default="time.csv",
            type=str,
            help="Path where to save the computation time of the different scores.",
        )
        parser.add_argument(
            "--verbose",
            dest="verbose",
            default=False,
            action="store_true",
            help="Whether to output the debug logs.",
        )
        parser.add_argument(
            "--log_path",
            dest="log_path",
            default="out.log",
            type=str,
            help="Path where to save the logs of the program.",
        )
        return parser.parse_args()

    @staticmethod
    def convert_cli_scores(all_scores: Optional[Union[str, List]]) -> List[ScoreAbstract]:
        """
        Convert command line arguments to a list of score instances
        :param all_scores: "ALL", "METRICS", "ENERGIES", or specific scores separated by a comma
        :return: List of instantiate scores
        """
        all_scores_class = []
        all_scores = "ALL" if all_scores is None else all_scores
        score_conversion = {
            "ALL": list(CONVERT_NAME_TO_SCORING_CLASS.keys()),
            "METRICS": LIST_ALL_METRICS,
            "ENERGIES": LIST_ALL_ENERGIES,
        }
        if isinstance(all_scores, list):
            all_scores_split = []
            for subscore in all_scores:
                if subscore in CONVERT_NAME_TO_SCORING_CLASS:
                    all_scores_split.append(subscore)
                elif subscore in score_conversion:
                    all_scores_split.extend(score_conversion[subscore])
        else:
            if all_scores in score_conversion:
                all_scores_split = score_conversion[all_scores]
            else:
                all_scores_split = all_scores  # type: ignore
        all_scores_name: str = ", ".join(all_scores_split)
        logger.info(f"Using the following scores: {all_scores_name}")
        for score_n in all_scores_split:
            if score_n in CONVERT_NAME_TO_SCORING_CLASS:
                all_scores_class.append(
                    CONVERT_NAME_TO_SCORING_CLASS.get(score_n)()  # type: ignore
                )
        return all_scores_class

    @staticmethod
    def convert_cli_args_scores(all_scores: str, *args, **kwargs) -> Dict:
        """
        Convert the inputs from cli of the scores to a list of associated score instances
        :param all_scores: names of the scores to use separated by a comma. It can also be `ALL`.
        :return: dictionary with the parameters to initialise the class.
        """
        all_scores_class = RNAdvisorCLI.convert_cli_scores(all_scores)
        arguments = {**kwargs, **{"all_scores": all_scores_class}}
        return arguments

    @staticmethod
    def get_bin_paths(yaml_content: Dict) -> Dict:
        """
        Return the bin paths from the yaml hp
        :param yaml_content: the dictionary from the '.yaml' file
        :return: dictionary with the bin paths
        """
        bin_paths = yaml_content.get("BIN_PATHS", None)
        if bin_paths is None:
            return {}
        # MC-Annotate binary path
        mc_annotate_bin = bin_paths.get("RNA_ASSESSMENT", None)
        # Path to the binary file of TMScore script
        zhang_bin_path = bin_paths.get("ZHANG_GROUP", None)
        # Path to the binary file of DFIRE-RNA
        dfire_bin_path = bin_paths.get("DFIRE", None)
        # Path to the binary file of MCQ4Structure
        mcq_bin_path = bin_paths.get("MCQ4STRUCTURES", None)
        # Path to the binary file of RASP
        rasp_bin_path = bin_paths.get("RASP", None)
        # Path to the rsRNASP binary file
        rs_rnasp_bin_path = bin_paths.get("rsRNASP", None)
        return {
            "mc_annotate_bin": mc_annotate_bin,
            "zhang_bin_path": zhang_bin_path,
            "dfire_bin_path": dfire_bin_path,
            "mcq_bin_path": mcq_bin_path,
            "rasp_bin_path": rasp_bin_path,
            "rs_rnasp_bin_path": rs_rnasp_bin_path,
        }

    @staticmethod
    def convert_cli_args(config_path: Optional[str], *args, **kwargs) -> Dict:
        """
        Convert the .yaml file to arguments readable by the class.
        :param config_path: Path to the config.yaml file with the different parameters.
        :return: a dictionary with the corresponding parameters to instantiate the class
        """
        if config_path is None:
            # Initialise with the arguments of the command line
            return RNAdvisorCLI.convert_cli_args_scores(*args, **kwargs)
        yaml_content = read_yaml_to_dict(config_path)
        # Arguments for the CLI
        score_hp = yaml_content.get("SCORE_HP", {})
        pred_path, native_path, result_path, time_path, verbose, log_path = (
            score_hp.get("PRED_PATH", None),
            score_hp.get("NATIVE_PATH", None),
            score_hp.get("RESULT_PATH", None),
            score_hp.get("TIME_PATH", None),
            score_hp.get("VERBOSE", False),
            score_hp.get("LOG_PATH", "out.log"),
        )
        normalise, sort_by = score_hp.get("NORMALISATION", True), score_hp.get("SORT_BY", None)
        all_scores = score_hp.get("ALL_SCORES", None)
        bin_paths = RNAdvisorCLI.get_bin_paths(yaml_content)
        all_scores = RNAdvisorCLI.convert_cli_scores(all_scores)
        config = {
            "pred_path": pred_path,
            "native_path": native_path,
            "result_path": result_path,
            "all_scores": all_scores,
            "normalise": normalise,
            "sort_by": sort_by,
            "time_path": time_path,
            "verbose": verbose,
            "log_path": log_path,
        }
        config = {**bin_paths, **config}
        return config

    def log_current_time(self, times: Dict):
        """
        Log the time spent for each method
        :param times: dictionary with the time spent for each method
        """
        all_times = list(times.values())
        c_times = 0
        names = ",".join(list(all_times[0].keys()))
        for element in all_times:
            for key, value in element.items():
                c_times += value
        logger.debug(f"TIME SPEND FOR {names} : {round(c_times, 5)} seconds")

    def compute_scores(self, mean_max_min: bool = False):
        """Compute all the scores and store them in the log file.
        Args:
            :param mean_max_min: whether to compute the min, max and mean for the different scores
        """
        all_scores, all_names, all_times = {}, [], {}  # type: ignore
        for score_fn in tqdm(self.all_scores):
            try:
                score, times = score_fn.compute(self.pred_path, self.native_path)
            except TypeError:
                logger.error(f"Error with {score_fn.__class__.__name__}")
                continue
            self.log_current_time(times)
            for path, c_scores in score.items():
                name = os.path.basename(path)
                for n_score, c_score in c_scores.items():
                    try:
                        c_score = round(c_score, 3) if n_score != "P-VALUE" else c_score
                    except (TypeError, IndexError):
                        c_score = np.nan
                    if name in all_scores:
                        all_scores[name].append(c_score)
                    else:
                        all_scores[name] = [c_score]
                    if n_score not in all_names:
                        all_names.append(n_score)
                    if n_score in all_times:
                        all_times[n_score].append(times[path][n_score])
                    else:
                        all_times[n_score] = [times[path][n_score]]
        if mean_max_min:
            mean_max_min_scores = self._compute_mean_max_min(all_scores)
            all_scores = {**all_scores, **mean_max_min_scores}
        score_df = pd.DataFrame(all_scores, index=all_names).T
        if self.sort_by in list(score_df.columns):
            logger.info(f"RESULTS SORTED BY {self.sort_by}")
            score_df.sort_values(by=[self.sort_by], inplace=True)
        times_df = pd.DataFrame(all_times, index=list(all_scores.keys()))
        self._save_scores(score_df, self.result_path, "Results")
        self._save_scores(times_df, self.time_path, "Times")
        if self.log_path is not None:
            logger.success(f"LOG PATH SAVED AT : {self.log_path}")

    def _compute_mean_max_min(self, all_scores: Dict) -> Dict:
        """
        Compute the mean, max and minimum for the different metrics
        :param all_scores:
        :return: new dictionary with new lines for mean, min and max
        """
        scores_matrix = np.array(list(all_scores.values()))
        score_min, score_max, score_mean = (
            np.nanmin(scores_matrix, axis=0).tolist(),
            np.nanmax(scores_matrix, axis=0).tolist(),
            np.nanmean(scores_matrix, axis=0).tolist(),
        )
        new_scores = {"Min": score_min, "Max": score_max, "Mean": score_mean}
        return new_scores

    def _save_scores(
        self, score_df: pd.DataFrame, result_path: Optional[str] = None, name: str = "Results"
    ):
        """
        Save the scores in a dataframe in the result_path
        :param score_df: the different scores to save
        """
        if result_path is None:
            logger.warning(f"NO {name.upper()} PATH, NO SAVING")
            return None
        score_df.to_csv(result_path)
        logger.success(f"{name} SAVED AT {result_path}")

    @staticmethod
    def normalize_structure(input_path: str, out_path: str) -> bool:
        """
        Normalize the .pdb structure to have standard conventions.
        :param input_path: the pdb file to normalize
        :param out_path: the pdb path where to save the normalized structure
        :return: a boolean that says if the normalisation has been done with success or not
        """
        basename = os.path.join("lib", "rna_assessment", "data")
        RESIDUES_LIST, ATOMS_LIST = os.path.join(basename, "residues.list"), os.path.join(
            basename, "atoms.list"
        )
        pdb_normalizer = PDBNormalizer(RESIDUES_LIST, ATOMS_LIST)
        is_ok = pdb_normalizer.parse(input_path, out_path)
        return is_ok


if __name__ == "__main__":
    args = RNAdvisorCLI.get_arguments()
    args = RNAdvisorCLI.convert_cli_args(**vars(args))
    score_cli = RNAdvisorCLI(**args)
    score_cli.compute_scores()
