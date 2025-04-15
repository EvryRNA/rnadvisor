"""
Class that implements the RNA3DCNN scoring function.

Original code from:
https://github.com/lijunRNA/RNA3DCNN

Original paper:
Li J, Zhu W, Wang J, Li W, Gong S, Zhang J, Wang W.
RNA3DCNN: Local and global quality assessments of RNA 3D structures using 3D deep
convolutional neural networks.
PLoS Comput Biol. 2018 Nov 27;14(11):e1006514.
doi: 10.1371/journal.pcbi.1006514. PMID: 30481171; PMCID: PMC6258470.
"""
from typing import Optional, Tuple, Dict
import tensorflow as tf

from Main import load_CNN_model, preprocess_input
from Bio.PDB.PDBParser import PDBParser
import numpy as np

from ModifyName import modify_residue_atom_name
from PixelateResidue import NBINS, pixelate_atoms_in_box



from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract

from rnadvisor.utils.utils import fn_time


class RNA3DCNNHelper(PredictAbstract):
    """
    Class that implements the ARES code.
    """

    def __init__(self, *args, **kwargs):
        super(RNA3DCNNHelper, self).__init__(name="rna3dcnn",*args, **kwargs)
        self.model_paths = {"RNA3DCNN-MD" : "RNA3DCNN_MD.hdf5", "RNA3DCNN-MDMC": "RNA3DCNN_MDMC.hdf5"}
        self.models = {key: load_CNN_model(value) for key, value in self.model_paths.items()}

    def predict_rna(self, rna_path: str, model_name: str) -> float:
        """
        Predict the RNA3DCNN score for a given RNA structure.
        :param rna_path: path to the RNA structure file
        :param model_name: name of the model to use
        :return:
        """
        p = PDBParser(QUIET=True)
        s = p.get_structure(rna_path, rna_path)
        model = s[0]
        residues = list(model.get_residues())
        length = len(residues)
        modify_residue_atom_name(residues)
        pixels = np.zeros((length, 3, NBINS, NBINS, NBINS))
        pixels = pixelate_atoms_in_box(model, pixels)
        pixels = preprocess_input(pixels)
        model = self.models[model_name]
        try:
            score_residue = model.predict(pixels)
            score = np.sum(score_residue)
        except tf.errors.InvalidArgumentError as e:
            score = np.nan
        return score

    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
    ) -> Tuple[Dict, Dict]:
        out_scores, out_times = {}, {}
        for model_name in self.models.keys():
            score, c_time = fn_time(
                self.predict_rna,
                pred_path,
                model_name,
            )
            out_scores[model_name] = score
            out_times[model_name] = c_time
        return out_scores, out_times

main = build_predict_cli(RNA3DCNNHelper)

if __name__ == "__main__":
    main()
