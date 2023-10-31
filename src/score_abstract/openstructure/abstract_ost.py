import json
import subprocess

import numpy as np

from src.score_abstract.score_abstract import ScoreAbstract


COMMAND = "ost compare-structures -r $NATIVE_PATH -m $PRED_PATH -o tmp/out.json"


class AbstractOST(ScoreAbstract):
    """
    Class that is used to compute the scores using the OpenStructure library.
    """

    def __init__(self, *args, **kwargs):
        super(AbstractOST, self).__init__(*args, **kwargs)

    @staticmethod
    def _get_metric_from_json(metric: str) -> float:
        """Return the metric from the json file."""
        with open("tmp/out.json", "r") as f:
            data = json.load(f)
        metric = metric.replace("-", "_").replace("qs_score", "qs_global")
        return data.get(metric.replace("-", "_"), np.nan)

    @staticmethod
    def get_metric(pred_path: str, native_path: str, metric: str) -> float:
        """
        Return the score given metric.
        """
        command = COMMAND.replace("$NATIVE_PATH", native_path).replace("$PRED_PATH", pred_path)
        command += f" --{metric}"
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return AbstractOST._get_metric_from_json(metric)
