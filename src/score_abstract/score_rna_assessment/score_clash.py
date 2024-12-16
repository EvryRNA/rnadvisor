"""
Implementation of the CLASH score.
It gives the number of bad overlaps per 1000 atoms

The original paper is:
Davis, I. W., Leaver-Fay, A., Chen, V. B., Block, J. N., Kapral, G. J., Wang, X.,
Murray, L. W., Arendall, W. B., Snoeyink, J., Richardson, J. S., & Richardson, D. C.
(2007).
MolProbity: all-atom contacts and structure validation for proteins and nucleic acids.
Nucleic Acids Research, 35(Web Server), W375–W383.
https://doi.org/10.1093/nar/gkm216

Implementation from
    https://github.com/RNA-Puzzles/rna-tools/blob/master/rna_tools/tools/ClashCalc/ClashCalc.py
"""

from typing import Dict, Tuple

import numpy as np
from Bio.PDB import Atom, NeighborSearch
from loguru import logger

from src.score_abstract.score_abstract import ScoreAbstract
from src.utils import time_it


class ScoreClash(ScoreAbstract):
    def __init__(self, *args, **kwargs):
        super(ScoreClash, self).__init__(*args, **kwargs)

    @staticmethod
    def compute_clash_score(pred_path: str) -> float:
        """
        Compute the clash score: number of bad overlaps per 1000 atoms
        Code from
        https://github.com/RNA-Puzzles/rna-tools/blob/master/rna_tools/tools/ClashCalc/ClashCalc.py
        :param pred_path: the path to the .pdb file of a prediction.
        :return: the clash score
        """
        structure = open(pred_path)
        atoms_a, atoms_b = [], []
        for line in structure.readlines():
            if line[:4] == "ATOM":
                at_nam = line[12:16].strip()
                coor = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
                at = Atom.Atom(at_nam, coor, 0.0, 1.0, " ", at_nam, 1, at_nam[0])
                if line[21] == "A":
                    atoms_a.append(at)
                elif line[21] == "B":
                    atoms_b.append(at)
                else:
                    pass
        if len(atoms_a) > len(atoms_b):
            less = atoms_b
            more = atoms_a
        else:
            less = atoms_a
            more = atoms_b
        problem = 0
        contacts = 0
        ns = NeighborSearch(more)
        for at in less:
            neighbors = ns.search(np.array(at.get_coord()), 2.0, "A")
            if neighbors != []:
                problem += 1
                contacts += 1
            else:
                neighbors1 = ns.search(np.array(at.get_coord()), 4.0, "A")
                if neighbors1 != []:
                    contacts += 1
        try:
            fract = float(problem) / float(contacts)
            fract = round(fract, 3)
        except ZeroDivisionError:
            fract = problem  # or skip this structure
            logger.debug(f"Zero division in CLASH score : {pred_path}, {problem}, {contacts}")
        return fract

    @time_it
    def _compute(self, pred_path: str, native_path: str) -> Tuple[Dict, Dict]:
        """
        Compute the clash score from RNA_Assessment implementation
        :param pred_path: the path to the .pdb file of a prediction.
        :param native_path: the path to the .pdb file of the native structure.
        :return: the clash score
        """
        try:
            clash_score = self.compute_clash_score(pred_path)
        except IndexError:
            clash_score = np.nan
        return {"CLASH": clash_score}  # type: ignore
