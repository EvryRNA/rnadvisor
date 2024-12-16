from typing import Any, List, Dict
from Bio.PDB import Atom, Model, Chain, Residue, Structure, PDBIO
import Bio
import numpy as np
from Bio.PDB import Atom, Residue, PDBParser
import warnings

warnings.filterwarnings("ignore")


def read_all_atoms(in_pdb: str) -> Any:
    """
    Read and return the coordinates of all the  atoms from a pdb file
    :param in_pdb: path to a .pdb file
    """
    parser = PDBParser()
    all_atoms = []
    structure = parser.get_structure("", in_pdb)
    for model in structure:
        for chain in model:
            for residue in chain:
                res = residue.get_resname().replace(" ", "")
                if res in ["A", "C", "G", "U"]:
                    atoms = get_atoms_torsion(residue)
                    c_atom = {atom.get_name(): atom.get_coord().tolist() for atom in atoms}
                    all_atoms.append(c_atom)
    return all_atoms


def get_atoms_torsion(residue: Bio.PDB.Residue.Residue):
    """
    Return the atoms coordinates for a given residue.
    :param residue: the residue to get the atoms from
    """
    atoms = []
    for atom in residue:
        atoms.append(atom)
    return atoms


def compute_torsion_angle(
    atom1: np.ndarray, atom2: np.ndarray, atom3: np.ndarray, atom4: np.ndarray
) -> float:
    """
    Compute torsional angles between 4 atoms
    :return: the torsional angles between the atoms
    """
    v12 = atom1 - atom2
    v23 = atom2 - atom3
    v34 = atom3 - atom4
    e1 = np.cross(v12, v23)
    e2 = np.cross(v23, v34)
    sign = +1 if np.dot(v23, np.cross(e1, e2)) < 0 else -1
    angle_in_radians = np.arccos(np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2)))
    angle_in_degrees = sign * np.degrees(angle_in_radians)
    return angle_in_degrees


def get_sequence(in_pdb: str) -> str:
    """
    Return the RNA sequence from a .pdb file
    :param in_pdb: path to a pdb file
    :return: RNA sequence of nucleotides
    """
    parser = PDBParser()
    structure = parser.get_structure("structure", in_pdb)
    sequence = ""
    for model in structure:
        for chain in model:
            for residue in chain:
                res = residue.get_resname().replace(" ", "")
                if res in ["A", "C", "G", "U"]:
                    sequence += res
    return sequence
