from typing import Dict

SERVICES = [
    "clash",
    "pamnet",
    "lociparse",
    "3drnascore",
    "tb-mcq",
    "barnaba",
    "cgrnasp",
    "dfire",
    "mcq",
    "lcs",
    "tm-score",
    "lddt",
    "rasp",
    "rs-rnasp",
    "rmsd",
    "inf",
    "p-value",
    "di",
    "gdt-ts",
    "cad-score",
    "ares",
    # "rna3dcnn",
    # "rna-briq",
]
ALL = SERVICES
ALL_METRICS = [
    "barnaba",
    "mcq",
    "lcs",
    "cad-score",
    "tm-score",
    "lddt",
    "rmsd",
    "inf",
    "p-value",
    "di",
    "gdt-ts",
    "cad_score",
    "clash",
]
ALL_SF = [
    "pamnet",
    "lociparse",
    "3drnascore",
    "tb-mcq",
    "barnaba",
    "cgrnasp",
    "dfire",
    "rasp",
    "rs-rnasp",
    "ares",
    # "rna3dcnn",
    # "rna-briq",
]

SERVICES_DICT: Dict = {key: {"args": {}} for key in SERVICES}


DESCENDING_METRICS = [
    "BARNABA-eRMSD",
    "BARNABA-RMSD",
    "RMSD",
    "P-VALUE",
    "CLASH",
    "MCQ",
    "RMSD",
    "DI",
]
DESCENDING_SF = [
    "PAMNet",
    "3drnascore",
    "tb_mcq",
    "cgRNASP",
    "cgRNASP-C",
    "cgRNASP-PC",
    "DFIRE",
    "RASP-ENERGY",
    "rsRNASP",
    "ARES",
]
