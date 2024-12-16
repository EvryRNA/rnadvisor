import numpy as np
from typing import List

from src.score_abstract.tb_mcq.enums.atoms import ANGLES, ALL_ATOMS
from src.score_abstract.tb_mcq.utils.utils import compute_torsion_angle


class ComputationHelper:
    def __init__(self, matrix: np.ndarray, sequence: str):
        self.matrix = matrix
        self.sequence = sequence

    def compute_angles(self, angle_name: str) -> List:
        """
        Compute all the angles for the given structure.
        :param angle_name: the angle to compute values from
        :return: a list with the angle values
        """
        c_angle_dict = ANGLES.get(angle_name, {})
        atoms = c_angle_dict.get("atoms", [])
        atoms_position = [ALL_ATOMS.index(atom) for atom in atoms]
        indexes = c_angle_dict.get("index", [])
        angles_out = []
        for i, c_atoms in enumerate(self.matrix):
            if angle_name == "chi" and self.sequence[i] in ["A", "G"]:
                atoms_position = [ALL_ATOMS.index(atom) for atom in ["O4'", "C1'", "N9", "C4"]]
            if angle_name == "chi" and self.sequence[i] in ["C", "U"]:
                atoms_position = [ALL_ATOMS.index(atom) for atom in ["O4'", "C1'", "N1", "C2"]]
            specific_atoms = [
                self.matrix[i + offset, atom_pos]
                for offset, atom_pos in zip(indexes, atoms_position)
                if i + offset < len(self.matrix) and i + offset >= 0
            ]
            angle = compute_torsion_angle(*specific_atoms) if len(specific_atoms) == 4 else np.nan
            angles_out.append(angle)
        return angles_out
