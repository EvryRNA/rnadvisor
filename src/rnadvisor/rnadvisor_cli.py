import json
import os
import shutil
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, no_type_check

import Bio.PDB
import click
import pandas as pd
from loguru import logger

from rnadvisor.enums.list_dockers import (
    DESCENDING_METRICS,
    DESCENDING_SF,
    SERVICES_DICT,
)
from rnadvisor.predict_abstract import PredictAbstract
from rnadvisor.utils.docker_helper import (
    run_services_docker,
)
from rnadvisor.utils.utils import (
    check_scores,
    clean_structure_rna_tools,
    convert_cif_to_pdb,
    init_logger,
)


@dataclass
class RNAdvisorCLI:
    pred_dir: str
    scores: List[str]
    out_path: Optional[str] = None
    native_path: Optional[str] = None
    out_time_path: Optional[str] = None
    sort_by: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    tmp_dir: Optional[str] = "/tmp/rnadvisor"  # nosec
    tmp_dir_out: Optional[str] = None
    tmp_dir_out_times: Optional[str] = None
    verbose: int = 1
    z_score: bool = False
    normalise: bool = False

    def __post_init__(self):
        init_logger(self.verbose)
        self.init_tmp_dir()
        self.clean_prev_results()
        self.check_init_paths(self.native_path, self.pred_dir)
        self.native_path, self.pred_dir = self.clean_pdb(
            self.native_path, self.pred_dir
        )
        self.scores = check_scores(self.scores)
        self.volumes = self.add_volumes()
        self.init_params()

    def init_params(self):
        """
        Initialize the parameters for the different scoring functions.
        """
        if self.params is None:
            self.params = {}
        if isinstance(self.params, str):
            try:
                self.params = json.loads(self.params)
            except json.JSONDecodeError:
                logger.warning("Invalid JSON string for params. Using empty dict.")
                self.params = {}
        if not isinstance(self.params, dict):
            logger.warning("Invalid type for params. Using empty dict.")
            self.params = {}

    def convert_cif_files_to_pdb(
        self, native_path: Optional[str], pred_dir: Optional[str]
    ) -> Tuple[Optional[str], Optional[str]]:
        """Convert .cif files to .pdb if needed. Only handle .pdb files if .cif are present."""
        if native_path and native_path.endswith(".cif"):
            convert_cif_to_pdb(native_path, self.clean_cif_native_path)  # type: ignore
            logger.info(f"Converted {native_path} to {self.clean_cif_native_path}")
            native_path = self.clean_cif_native_path
        if pred_dir:
            pred_dir = (
                os.path.dirname(pred_dir) if os.path.isfile(pred_dir) else pred_dir
            )
            cif_files = [f for f in os.listdir(pred_dir) if f.endswith(".cif")]
            if cif_files:
                os.makedirs(self.clean_cif_pred_dir, exist_ok=True)
                for f in cif_files:
                    in_path = os.path.join(pred_dir, f)
                    out_path = os.path.join(
                        self.clean_cif_pred_dir, f.replace(".cif", ".pdb")
                    )
                    convert_cif_to_pdb(in_path, out_path)
                    logger.info(f"Converted {in_path} to {out_path}")
                pdb_files = [f for f in os.listdir(pred_dir) if f.endswith(".pdb")]
                for f in pdb_files:
                    src = os.path.join(pred_dir, f)
                    dst = os.path.join(self.clean_cif_pred_dir, f)
                    shutil.copyfile(src, dst)
                pred_dir = self.clean_cif_pred_dir
        return native_path, pred_dir

    def clean_pdb(
        self, native_path: Optional[str], pred_dir: Optional[str]
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Clean the structures and make them ready for the assessment.
        Convert .cif to .pdb if needed.
        """
        native_path, pred_dir = self.convert_cif_files_to_pdb(native_path, pred_dir)
        if not self.normalise:
            return native_path, pred_dir
        if native_path is not None:
            try:
                clean_structure_rna_tools(native_path, self.clean_native_path)
                native_path = self.clean_native_path
            except (
                Bio.PDB.PDBExceptions.PDBConstructionException,
                KeyError,
                UnboundLocalError,
            ):
                logger.warning(
                    f"Error cleaning {native_path}. Copying the original file."
                )
        if pred_dir is not None:
            if os.path.isfile(pred_dir):
                pred_dir = os.path.dirname(pred_dir)
            rnas = [name for name in os.listdir(pred_dir) if name.endswith(".pdb")]
            for rna in rnas:
                in_path = os.path.join(pred_dir, rna)
                out_path = os.path.join(self.clean_pred_dir, rna)
                try:
                    clean_structure_rna_tools(in_path, out_path)
                except (
                    Bio.PDB.PDBExceptions.PDBConstructionException,
                    KeyError,
                    UnboundLocalError,
                ):
                    logger.warning(
                        f"Error cleaning {in_path}. Copying the original file."
                    )
                    shutil.copy(in_path, out_path)
            pred_dir = self.clean_pred_dir
        return native_path, pred_dir

    def init_tmp_dir(self):
        """
        Create a tmp directory where to store the outputs of the different docker containers.
        """
        unique_id = uuid.uuid4().hex[:8]
        out_dir = os.path.join(self.tmp_dir, f"run_{unique_id}")
        self.tmp_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)
        self.tmp_dir_out = os.path.join(out_dir, "scores")
        self.tmp_dir_out_times = os.path.join(out_dir, "times")
        tmp_clean_dir = os.path.join(out_dir, "clean_pdb")
        tmp_cif = os.path.join(out_dir, "cif")
        self.clean_cif_native_path = os.path.join(tmp_cif, "native.pdb")
        self.clean_cif_pred_dir = os.path.join(tmp_cif, "preds")
        self.clean_native_path = os.path.join(tmp_clean_dir, "native.pdb")
        self.clean_pred_dir = os.path.join(tmp_clean_dir, "preds")
        self.dc_path = os.path.join(self.tmp_dir, "docker-compose.yml")
        os.makedirs(self.clean_cif_pred_dir, exist_ok=True)
        os.makedirs(self.tmp_dir_out, exist_ok=True)
        os.makedirs(self.tmp_dir_out_times, exist_ok=True)
        os.makedirs(tmp_clean_dir, exist_ok=True)
        os.makedirs(self.clean_pred_dir, exist_ok=True)

    def add_volumes(self) -> Dict[str, str]:
        """
        Return a dict mapping host absolute paths to container paths.
        """
        volumes = {}

        def bind_path(host_path: str, container_path: str):
            if host_path:
                abs_host = os.path.abspath(host_path)
                volumes[abs_host] = container_path

        if self.native_path is not None and os.path.isfile(self.native_path):
            bind_path(self.native_path, "/data/native.pdb")
        if self.pred_dir is not None:
            bind_path(self.pred_dir, "/data/preds")
        if self.tmp_dir is not None:
            bind_path(self.tmp_dir_out, "/app/tmp/results")  # type: ignore
        if self.tmp_dir_out_times is not None:
            bind_path(self.tmp_dir_out_times, "/app/tmp/results_time")
        return volumes

    def clean_prev_results(self):
        """
        Remove the previous results if they exist.
        """
        shutil.rmtree(self.tmp_dir_out, ignore_errors=True)
        shutil.rmtree(self.tmp_dir_out_times, ignore_errors=True)

    def check_init_paths(self, native_path: Optional[str], pred_dir: Optional[str]):
        """
        Check the different paths depending if there is a native path or not
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_dir: path to a directory or single RNA `.pdb` file.
        """
        if native_path is None and pred_dir is None:
            msg = "Either native_path or pred_dir must be provided."
            logger.warning(msg)
            raise ValueError(msg)
        elif native_path is not None and pred_dir is None:
            logger.info(
                f"No prediction directory provided. Using native path: {native_path}"
            )
        elif native_path is not None and pred_dir is not None:
            if os.path.isfile(pred_dir):
                logger.info(f"Using prediction file: {pred_dir}")
                return None
            if not os.path.isdir(pred_dir):
                raise ValueError(
                    f"Prediction directory {pred_dir} is not a valid file or directory."
                )
            if os.path.exists(native_path):
                logger.info(
                    f"Using native path: {native_path} and prediction directory: {pred_dir}"
                )
            else:
                logger.warning(
                    f"Native path {native_path} does not exist. Using prediction directory: {pred_dir}"
                )
        elif native_path is None and pred_dir is not None:
            if not (os.path.isdir(pred_dir) or os.path.isfile(pred_dir)):
                raise ValueError(
                    f"Prediction directory {pred_dir} is not a valid file or directory."
                )
            logger.info(f"Using prediction directory: {pred_dir}")

    def get_services(self) -> Dict:
        """
        Get the different docker services to run
        :return: a dictionary of services
        """
        services = {}
        for key in self.scores:
            service = SERVICES_DICT[key]
            params = (
                json.dumps(self.params)
                if isinstance(self.params, dict)
                else self.params
                if isinstance(self.params, str) and self.params.strip()
                else None
            )
            service["args"].update(
                {
                    "--native_path": "/data/native.pdb"
                    if self.native_path is not None and os.path.isfile(self.native_path)
                    else "",
                    "--pred_dir": "/data/preds" if self.pred_dir is not None else "",
                    "--params": params,
                    "--out_path": f"/app/tmp/results/{key}.csv"
                    if self.tmp_dir_out is not None
                    else "",
                    "--out_time_path": f"/app/tmp/results_time/{key}.csv"
                    if self.tmp_dir_out_times is not None
                    else "",
                }
            )
            services[key] = service
        return services

    @no_type_check
    def merge_dfs(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Merge all the predicted dataframes into a single dataframe
        :return: the merged dataframes with all the scores
        """
        df_scores, df_times = None, None
        try:
            csvs = [
                os.path.join(self.tmp_dir_out, name)
                for name in os.listdir(self.tmp_dir_out)
                if name.endswith(".csv")
            ]
            csvs_times = [
                os.path.join(self.tmp_dir_out_times, name)
                for name in os.listdir(self.tmp_dir_out_times)
                if name.endswith(".csv")
            ]
            df_scores = pd.concat(
                [pd.read_csv(f, index_col=0) for f in csvs], axis=1
            ).round(2)
            df_times = pd.concat(
                [pd.read_csv(f, index_col=0) for f in csvs_times], axis=1
            ).round(2)
        except (PermissionError, FileNotFoundError):
            logger.warning("No scores or times found. Returning empty dataframes.")
        shutil.rmtree(self.tmp_dir_out_times, ignore_errors=True)
        shutil.rmtree(self.tmp_dir_out, ignore_errors=True)
        return df_scores, df_times

    def postprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute the Z-score if provided and sort based on the argument sort_by
        :param df: output dataframe from the predicted scores
        :return: a new dataframe with Z-score if provided.
        """
        if self.z_score:
            df = self.compute_z_score(df)
        if self.sort_by is not None:
            if self.sort_by not in df.columns:
                logger.warning(
                    f"Sort by {self.sort_by} not in dataframe. Returning original dataframe."
                )
                return df
            df = df.sort_values(by=self.sort_by, ascending=False)
        df = df.round(2)
        return df

    def compute_z_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute the Z-score:
            Z-score = (X - mean) / std
        :param df: dataframe with the different scoring functions
        :return: new dataframe with the Z-score for each metric/scoring function
        """
        z_df = (df - df.mean(skipna=True)) / df.std(skipna=True)
        # Compute Z-Score
        for col in df.columns:
            if col in DESCENDING_METRICS or col in DESCENDING_SF:
                z_df[col] = -z_df[col]
        for col in df.columns:
            df[f"Z-{col}"] = z_df[col]
        return df

    def save_dfs(
        self,
        df: pd.DataFrame,
        df_times: pd.DataFrame,
        out_path: Optional[str],
        out_time_path: Optional[str],
    ):
        """
        Save the output dictionary into dataframes
        :param df: predicted scores
        :param df_times: time for each RNA
        :param out_path: path where to save the predictions
        :param out_time_path: path where to save the times for each prediction
        """
        out_path, out_time_path = PredictAbstract.init_out_path(out_path, out_time_path)
        if df is None:
            logger.warning("No scores found")
            return None
        logger.info(f"Saving predictions to {out_path}")
        df = self.postprocess(df)
        df.to_csv(out_path, index=True)
        logger.info(f"Saving time to {out_time_path}")
        df_times.to_csv(out_time_path, index=True)

    def predict(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run the predictions for the different metrics/scoring functions
        :return:
        """
        services = self.get_services()
        run_services_docker(services, self.volumes, self.verbose, self.dc_path)
        try:
            df, df_times = self.merge_dfs()
        except ValueError:
            logger.warning("No scores found. Returning empty dataframes.")
            df, df_times = pd.DataFrame(), pd.DataFrame()
        self.save_dfs(df, df_times, self.out_path, self.out_time_path)
        if os.path.exists(self.tmp_dir):  # type: ignore
            shutil.rmtree(self.tmp_dir, ignore_errors=True)  # type: ignore
        return df, df_times

    def __call__(self):
        """
        Run the RNAdvisor CLI
        """
        self.predict()


@click.command()
@click.option(
    "--native_path", type=str, default=None, help="Path to the native structure."
)
@click.option(
    "--pred_dir", type=str, required=True, help="Path to the prediction directory."
)
@click.option(
    "--out_path", type=str, default="out.csv", help="Path to save the results."
)
@click.option(
    "--out_time_path", type=str, default=None, help="Path to save the time results."
)
@click.option(
    "--scores",
    type=str,
    default="lociparse",
    help="Comma-separated list of scores to compute.",
    callback=lambda ctx, param, value: value.split(","),
)
@click.option("--sort_by", type=str, default=None, help="Sort by a specific score.")
@click.option(
    "--params",
    type=str,
    default=None,
    help="Additional parameters for scoring functions.",
)
@click.option(
    "--tmp_dir",
    type=str,
    default="/tmp/rnadvisor",  # nosec
    help="Where to store the tmp predictions.",
)
@click.option(
    "--verbose",
    type=int,
    default=1,
    help="Verbose level: 0 (no output), 1 (info), 2 (debug).",
)
@click.option(
    "--z_score", is_flag=True, help="Whether to compute Z-score among the scores."
)
@click.option(
    "--normalise",
    is_flag=True,
    help="Whether to use RNA-tools rna-puzzles-ready function or not.",
)
def main(
    native_path,
    pred_dir,
    out_path,
    out_time_path,
    scores,
    sort_by,
    params,
    tmp_dir,
    verbose,
    z_score,
    normalise,
):
    """
    Main function to run the RNAdvisor CLI
    :param native_path: path to the native structure.
    :param pred_dir: path to the prediction directory.
    :param out_path: path to save the results.
    :param out_time_path: path to save the time results.
    :param scores: list of scores to compute.
    :param sort_by: sort by a specific score.
    :param params: additional parameters for scoring functions.
    :param tmp_dir: where to store the tmp predictions.
    :param verbose: verbose level: 0 (no output), 1 (info), 2 (debug).
    :param z_score: whether to compute Z-score among the scores.
    :param normalise: whether to use RNA-tools rna-puzzles-ready function or not.
    """
    rnadvisor_cli = RNAdvisorCLI(
        native_path=native_path,
        pred_dir=pred_dir,
        out_path=out_path,
        out_time_path=out_time_path,
        scores=list(scores),
        sort_by=sort_by,
        params=params,
        tmp_dir=tmp_dir,
        verbose=verbose,
        z_score=z_score,
        normalise=normalise,
    )
    rnadvisor_cli.predict()


if __name__ == "__main__":
    main()
