"""
Code that implement the RASP algorithm. It is based on http://melolab.org/webrasp/download.php.
I've created a fork of the project where I summarized the installation process:
            https://github.com/clementbernardd/rasp_rna
Reference:
Capriotti E, Norambuena T, Marti-Renom MA, Melo F.
(2011) All-atom knowledge-based potential for RNA structure prediction and assessment.
Bioinformatics 27(8):1086-93
"""

import os
import subprocess
import time
from typing import Dict, Optional, Tuple, List

from rnadvisor.cli_runner import build_predict_cli
from rnadvisor.predict_abstract import PredictAbstract



class RASPHelper(PredictAbstract):
    def __init__(self, rasp_bin_path: Optional[str] = None, *args, **kwargs):
        super(RASPHelper, self).__init__(name="rasp", *args, **kwargs)
        self.rasp_bin_path = rasp_bin_path

    @staticmethod
    def compute_rasp(pred_path: str, rasp_bin_path: Optional[str] = None) -> List:
        """
        Compute the RASP free energy.
        :param pred_path: path to a .pdb file
        :param rasp_bin_path: binary path to the rasp_fd file
        :return: the Energy Score, the Number of Contacts and the Normalized Energy.
        Refer to http://melolab.org/webrasp/howto.php for the instruction of outputs.
        """
        rasp_bin_path = (
            rasp_bin_path
            if rasp_bin_path is not None
            else os.path.join("lib", "rasp", "bin", "rasp_fd")
        )
        command = (
                f"{rasp_bin_path} -e all -p {pred_path}" + """ | awk '{print $1 " " $2 " " $3}'"""
        )
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        rasp = output.decode().replace("\n", "").split()
        rasp = [float(score) for score in rasp]  # type: ignore
        return rasp

    def predict_single_file(
            self, native_path: Optional[str], pred_path: str, *args, **kwargs
        ) -> Tuple[Dict, Dict]:
        time_b = time.time()
        energy_score, nb_contacts, normalized_energy = self.compute_rasp(
            pred_path, self.rasp_bin_path
        )
        execution_time = time.time() - time_b
        scores = {
            "RASP-ENERGY": energy_score,
            "RASP-NB-CONTACTS": nb_contacts,
            "RASP-NORMALIZED-ENERGY": normalized_energy,
        }
        times = {
            "RASP-ENERGY": execution_time,
            "RASP-NB-CONTACTS": execution_time,
            "RASP-NORMALIZED-ENERGY": execution_time,
        }
        return scores, times


main = build_predict_cli(RASPHelper)

if __name__ == "__main__":
    main()
