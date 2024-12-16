import os
from typing import Dict, List, Optional
import numpy as np

import pandas as pd

from src.score_abstract.tb_mcq.helper.computation_helper import ComputationHelper
from src.score_abstract.tb_mcq.enums.atoms import ALL_ATOMS, ANGLES
from src.score_abstract.tb_mcq.utils.utils import read_all_atoms, get_sequence


class ExtractorHelper:
    def __init__(self, all_atoms: List = ALL_ATOMS):
        self.all_atoms = all_atoms

    def extract_all(self, in_pdb: str, save_to_path: Optional[str] = None) -> pd.DataFrame:
        """
        Extract all the torsional angles and bond angles from the pdb file
        :param in_pdb: path to a .pdb file
        :param save_to_path: path where to save the output
        :return: a .csv file with the torsional and bond angles.
        """
        all_atoms = read_all_atoms(in_pdb)
        matrix = self.convert_atoms_to_matrix(all_atoms)
        sequence = [element for element in get_sequence(in_pdb)]
        computation_helper = ComputationHelper(matrix, sequence)
        torsion_angles = {angle: computation_helper.compute_angles(angle) for angle in ANGLES}
        sequence = [element for element in get_sequence(in_pdb)]
        df = pd.DataFrame(
            {**{"sequence": sequence}, **torsion_angles},
            index=range(1, len(sequence) + 1),
        )
        if save_to_path:
            df.to_csv(save_to_path)
        return df

    def convert_atoms_to_matrix(self, all_atoms: Dict) -> np.ndarray:
        """
        Convert the different atoms into a matrix of size (L, N, 3) where:
            L: the number of nucleotides
            N: the number of atoms per nucleotide
            3: the x,y,z coordinates
        :param all_atoms: list of atoms with their coordinates
        :return: a np.array matrix
        """
        output = np.nan * np.ones((len(all_atoms), len(self.all_atoms), 3))
        for index, atoms in enumerate(all_atoms):
            for atom in atoms:
                if atom in self.all_atoms:
                    output[index, self.all_atoms.index(atom)] = np.array(atoms[atom])
        return output
