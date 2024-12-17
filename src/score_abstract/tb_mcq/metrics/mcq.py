from typing import Union, List
import numpy as np
import pandas as pd

import warnings

warnings.filterwarnings("ignore")

TORSION_TO_ANGLES = {
    "BACKBONE": ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "chi", "phase"],
    "PSEUDO": ["eta", "theta"],
}


class MCQ:
    """
    MCQ Helper. Reproduce the MCQ computation from https://github.com/tzok/mcq4structures.
    """

    def mod(self, values: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
        """
        Compute the mod(t) = t + 2pi % 2pi
        Computation is done in degree
        :param values:
        :return:
        """
        return (values + 360) % 360

    def difference(self, x: float, y: float):
        """
        Compute the distance between two angles
        :param x: the true angle
        :param x: the predicted atom
        :return: the distance based on MCQ computation
        """
        if np.isnan(x) and np.isnan(y):
            return 0
        elif np.isnan(x) or np.isnan(y):
            return 180
        else:
            return min(abs(self.mod(x) - self.mod(y)), 360 - abs(self.mod(x) - self.mod(y)))

    def get_phase(self, values: np.ndarray):
        """
        Compute the phase P = arctan(v1 + v4 - v0 - v3, 2v2(sin 36 + sin72))
        :param values:
        :return:
        """
        try:
            riboses = np.radians(values[["v0", "v1", "v2", "v3", "v4"]])
            num = riboses["v1"] + riboses["v4"] - riboses["v0"] - riboses["v3"]
            denom = 2 * riboses["v2"] * (np.sin(np.radians(36)) + np.sin(np.radians(72)))
            P = np.arctan(num.values, denom.values)
        except KeyError:
            P = np.nan
        return P

    def compute_mcq(
        self, true_values: np.ndarray, pred_values: np.ndarray, torsion: str = "BACKBONE"
    ):
        """
        Compute the MCQ between two sets of angles.
        :param true_values: experimental inferred angles from the native structure
        :param pred_values: predicted angles
        :param torsion: the type of angles to use. Default to BACKBONE.
        :return:
        """
        diff, angles = self._get_diff_angles(true_values, pred_values, torsion)
        sin_mod, cos_mod = np.sin(np.radians(diff)).sum(), np.cos(np.radians(diff)).sum()
        mcq = np.arctan2(sin_mod, cos_mod)
        mcq = np.degrees(mcq)
        return mcq

    def get_current_angles(self, torsion: str, pred_cols: List):
        """
        Get the current angles values from all the angles available.
        """
        angles = []
        for angle in TORSION_TO_ANGLES[torsion]:
            if angle == "phase" and "v0" in pred_cols:
                angles.append(angle)
            elif angle in pred_cols:
                angles.append(angle)
        return angles

    def _get_diff_angles(self, true_values: pd.DataFrame, pred_values: pd.DataFrame, torsion: str):
        """
        Compute the differences to be used for the MCQ computation
        :return:
        """
        if len(pred_values) < len(true_values):
            true_values = true_values[: len(pred_values)]
        else:
            pred_values = pred_values[: len(true_values)]
        angles = self.get_current_angles(torsion, pred_values.columns)
        if torsion == "BACKBONE":
            phase_true = np.degrees(self.get_phase(true_values))
            phase_pred = np.degrees(self.get_phase(pred_values))
            true_values["phase"] = phase_true
            pred_values["phase"] = phase_pred
        true_angles = true_values[angles].values
        pred_angles = pred_values[angles].values
        diff_fn = np.vectorize(self.difference)
        diff = diff_fn(true_angles, pred_angles)
        return diff, angles

    def compute_mcq_per_angle(self, true_values, pred_values, torsion: str):
        """
        Compute the MCQ for a given angle.
        :param true_values: experimental inferred angles from the native structure
        :param pred_values: predicted angles
        :param torsion: the type of angles to use. Default to BACKBONE.
        :return: MCQ per angle
        """
        diff, angles = self._get_diff_angles(true_values, pred_values, torsion)
        sin_mod, cos_mod = np.sin(np.radians(diff)).sum(axis=0), np.cos(np.radians(diff)).sum(
            axis=0
        )
        mcq = np.arctan2(sin_mod, cos_mod)
        mcq = np.degrees(mcq)
        output = {angle: mcq[i] for i, angle in enumerate(angles)}
        return output

    def compute_mcq_per_sequence(self, true_values, pred_values, torsion: str):
        """
        Compute the MCQ for a given position.
        :return:
        """
        diff, angles = self._get_diff_angles(true_values, pred_values, torsion)
        sin_mod, cos_mod = np.sin(np.radians(diff)).sum(axis=1), np.cos(np.radians(diff)).sum(
            axis=1
        )
        mcq = np.arctan2(sin_mod, cos_mod)
        mcq = np.degrees(mcq)
        return mcq.tolist()
