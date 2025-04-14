import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple

import click
from loguru import logger
import pandas as pd
import os

from rnadvisor.enums.list_dockers import SERVICES, SERVICES_DICT

from rnadvisor.enums.list_dockers import OUT_DIR_SCORES,OUT_DIR_TIMES,OUT_DIR


@dataclass
class RNAdvisorCLI:
    native_path: Optional[str]
    pred_dir: str
    out_path: Optional[str]
    out_time_path: Optional[str]
    scores: List[str]
    sort_by: Optional[str]
    params: Optional[Dict[str, Any]]

    def __post_init__(self):
        self.check_init_paths(self.native_path, self.pred_dir)
        self.scores = self.check_scores(self.scores)
        self._init_logger()

    def _init_logger(self, verbose: bool = True):
        """
        Initialise the logger parameters.
        :param verbose: whether to print the debug logs in terminal
        """
        logger.remove()
        logger.add(sys.stderr, level="DEBUG" if verbose else "INFO")

    def check_scores(self, scores: List[str]) -> List[str]:
        """
        Check the given metrics/scoring functions to use
        :param scores: list of metrics/scoring functions to use
        :return: list of metrics/scoring functions that can be used
        """
        scores = [score.lower() for score in scores]
        return [score for score in scores if score in SERVICES]

    def check_init_paths(self, native_path: Optional[str], pred_dir: Optional[str]):
        """
        Check the different paths depending if there is a native path or not
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_dir: path to a directory or single RNA `.pdb` file.
        """
        if native_path is None and pred_dir is None:
            raise ValueError("Either native_path or pred_dir must be provided.")
        elif native_path is not None and pred_dir is None:
            logger.info(f"No prediction directory provided. Using native path: {native_path}")
        elif native_path is not None and pred_dir is not None:
            if not os.path.isdir(pred_dir):
                raise ValueError(f"Prediction directory {pred_dir} is not a valid file or directory.")
            logger.info(f"Using native path: {native_path} and prediction directory: {pred_dir}")
        elif native_path is None and pred_dir is not None:
            if not (os.path.isdir(pred_dir) or os.path.isfile(pred_dir)):
                raise ValueError(
                    f"Prediction directory {pred_dir} is not a valid file or directory.")
            logger.info(f"Using prediction directory: {pred_dir}")

    def get_services(self) -> Dict:
        """
        Get the different docker services to run
        :return: a dictionary of services
        """
        services = {}
        for key in self.scores:
            service = SERVICES_DICT[key]
            service["args"].update({
                "--native_path": self.native_path,
                "--pred_dir": self.pred_dir,
            })
            services[key] = service
        return services

    def run_services(self, services: Dict) -> List:
        """
        Return the different docker images to run
        :param services: a dictionary of services with the different arguments
        """
        processes = []
        for service, config in services.items():
            cmd = ["docker", "compose", "run", "--rm", service]
            for key, val in config["args"].items():
                cmd += [key, val]
            cmd+=["--quiet"]
            process = subprocess.Popen(cmd)
            processes.append((service, process))
        return processes

    def wait_services(self, processes: List):
        """
        Run and wait for the different docker images to finish
        :param processes: a list of processes to wait for
        """
        for service, process in processes:
            ret_code = process.wait()
            if ret_code == 0:
                logger.info(f"✅ {service} completed successfully ✅")
            else:
                logger.info(f"❌ {service} exited with error code {ret_code} ❌")

    def merge_dfs(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Merge all the predicted dataframes into a single dataframe
        :return: the merged dataframes with all the scores
        """
        df_scores, df_times = None, None
        try:
            csvs = [os.path.join(OUT_DIR_SCORES, name) for name in os.listdir(OUT_DIR_SCORES) if name.endswith(".csv")]
            csvs_times = [os.path.join(OUT_DIR_TIMES, name) for name in os.listdir(OUT_DIR_TIMES) if name.endswith(".csv")]
            df_scores = pd.concat([pd.read_csv(f, index_col=0) for f in csvs], axis=1)
            df_times = pd.concat([pd.read_csv(f, index_col=0) for f in csvs_times], axis=1)
            shutil.rmtree(OUT_DIR_SCORES)
            shutil.rmtree(OUT_DIR_TIMES)
            shutil.rmtree(OUT_DIR)
        except (PermissionError, FileNotFoundError) as e:
            logger.warning("No scores or times found. Returning empty dataframes.")
        return df_scores, df_times

    def save_dfs(self, df: pd.DataFrame, df_times: pd.DataFrame, out_path: Optional[str], out_time_path: Optional[str]):
        """
        Save the output dictionary into dataframes
        :param df: predicted scores
        :param df_times: time for each RNA
        :param out_path: path where to save the predictions
        :param out_time_path: path where to save the times for each prediction
        """
        if out_path is None:
            logger.info("Output path is None. Not saving predictions.")
            return None
        if df is None:
            logger.warning("No predictions found. Not saving predictions.")
            return None
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        os.makedirs(os.path.dirname(out_time_path), exist_ok=True)
        logger.info(f"Saving predictions to {out_path}")
        df.to_csv(out_path, index=True)
        logger.info(f"Saving time to {out_time_path}")
        df_times.to_csv(out_time_path, index=True)

    def build_docker_images(self):
        """
        Ensure all Docker images are built before running services.
        """
        logger.info("🔧 Building Docker images (if needed)...")
        result = subprocess.run(["docker", "compose", "build"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("❌ Failed to build Docker images")
            logger.error(result.stderr)
            logger.error(result.stdout)
            sys.exit(1)
        logger.info("✅ Docker images are ready.")

    def predict(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run the predictions for the different metrics/scoring functions
        :return:
        """
        self.build_docker_images()
        services = self.get_services()
        processes = self.run_services(services)
        self.wait_services(processes)
        df, df_times = self.merge_dfs()
        self.save_dfs(df, df_times, self.out_path, self.out_time_path)
        return df, df_times

@click.command()
@click.option("--native_path", type=str, default=None, help="Path to the native structure.")
@click.option("--pred_dir", type=str, required=True, help="Path to the prediction directory.")
@click.option("--out_path", type=str, default=None, help="Path to save the results.")
@click.option("--out_time_path", type=str, default=None, help="Path to save the time results.")
@click.option( "--scores", type=str, default="lociparse", help="Comma-separated list of scores to compute.",
    callback=lambda ctx, param, value: value.split(",")
)
@click.option("--sort_by", type=str, default=None, help="Sort by a specific score.")
@click.option("--params", type=str, default=None, help="Additional parameters for scoring functions.")
def main(native_path, pred_dir, out_path, out_time_path, scores, sort_by, params):
    """
    Main function to run the RNAdvisor CLI
    :param native_path: path to the native structure.
    :param pred_dir: path to the prediction directory.
    :param out_path: path to save the results.
    :param out_time_path: path to save the time results.
    :param scores: list of scores to compute.
    :param sort_by: sort by a specific score.
    :param params: additional parameters for scoring functions.
    """
    rnadvisor_cli = RNAdvisorCLI(
        native_path=native_path,
        pred_dir=pred_dir,
        out_path=out_path,
        out_time_path=out_time_path,
        scores=list(scores),
        sort_by=sort_by,
        params=params
    )
    rnadvisor_cli.predict()
