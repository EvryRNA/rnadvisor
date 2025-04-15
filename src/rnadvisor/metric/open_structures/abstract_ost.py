import json
import subprocess

import os
from typing import List

import numpy as np


from rnadvisor.predict_abstract import PredictAbstract

COMMAND = "ost compare-structures -r $NATIVE_PATH -m $PRED_PATH -o tmp/out.json"


class AbstractOST(PredictAbstract):
    """
    Class that is used to compute the scores using the OpenStructure library.
    """

    def __init__(self, *args, **kwargs):
        super(AbstractOST, self).__init__(*args, **kwargs)
        os.makedirs("tmp", exist_ok=True)

    @staticmethod
    def _get_metric_from_json(metrics: List) -> List:
        """Return the metric from the json file."""
        with open("tmp/out.json", "r") as f:
            data = json.load(f)
        output = []
        for metric in metrics:
            c_metric = metric.replace("-", "_").replace("qs_score", "qs_global")
            value = data.get(c_metric.replace("-", "_"), np.nan)
            output.append(value)
        return output

    @staticmethod
    def get_metric(pred_path: str, native_path: str, metrics: List[str]) -> List:
        """
        Return the score given metric.
        """
        os.makedirs("tmp", exist_ok=True)
        metrics = [metrics] if isinstance(metrics, str) else metrics
        command = COMMAND.replace("$NATIVE_PATH", native_path).replace("$PRED_PATH", pred_path)
        command += "".join(f" --{m}" for m in metrics)
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return AbstractOST._get_metric_from_json(metrics)
