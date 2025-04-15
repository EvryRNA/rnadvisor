import os
OUT_DIR = os.path.join("data", "tmp")
OUT_DIR_SCORES = os.path.join("data", "tmp", "scores")
OUT_DIR_TIMES = os.path.join("data", "tmp", "times")

SERVICES = ["clash", "pamnet", "lociparse", "3drnascore",
            "tb_mcq", "barnaba", "cgrnasp",
            "dfire", "mcq", "lcs", "cad_score", "tm_score",
            "lddt", "rasp", "rs_rnasp", "rmsd", "inf",
            "p_value", "di", "gdt_ts", "cad_score"]
ALL = SERVICES
ALL_METRICS = ["barnaba", "mcq", "lcs", "cad_score", "tm_score",
           "lddt", "rmsd", "inf", "p_value", "di",
           "gdt_ts", "cad_score", "clash"]
ALL_SF = ["pamnet", "lociparse", "3drnascore",
          "tb_mcq", "barnaba", "cgrnasp", "dfire", "rasp",
          "rs_rnasp"]

SERVICES_DICT = {key: {"args": {
    "--out_path": os.path.join(OUT_DIR_SCORES, f"{key}.csv"),
    "--out_time_path": os.path.join(OUT_DIR_TIMES, f"{key}.csv"),
}} for key in SERVICES}