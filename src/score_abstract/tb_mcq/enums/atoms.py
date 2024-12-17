import numpy as np
import os

ALL_ATOMS = [
    "P",
    "OP1",
    "OP2",
    "O5'",
    "C5'",
    "C4'",
    "O4'",
    "C3'",
    "O3'",
    "C1'",
    "C2'",
    "N1",
    "C2",
    "N9",
    "C4",
]

ANGLES = {
    "alpha": {"atoms": ["O3'", "P", "O5'", "C5'"], "index": [-1, 0, 0, 0]},
    "beta": {"atoms": ["P", "O5'", "C5'", "C4'"], "index": [0, 0, 0, 0]},
    "gamma": {"atoms": ["O5'", "C5'", "C4'", "C3'"], "index": [0, 0, 0, 0]},
    "delta": {"atoms": ["C5'", "C4'", "C3'", "O3'"], "index": [0, 0, 0, 0]},
    "epsilon": {"atoms": ["C4'", "C3'", "O3'", "P"], "index": [0, 0, 0, 1]},
    "zeta": {"atoms": ["C3'", "O3'", "P", "O5'"], "index": [0, 0, 1, 1]},
    "chi": {"atoms": ["O4'", "C1'", "N1", "C2"], "index": [0, 0, 0, 0]},
    "eta": {"atoms": ["C4'", "P", "C4'", "P"], "index": [-1, 0, 0, 1]},
    "theta": {"atoms": ["P", "C4'", "P", "C4'"], "index": [0, 0, 1, 1]},
    "eta'": {"atoms": ["C1'", "P", "C1'", "P"], "index": [-1, 0, 0, 1]},
    "theta'": {"atoms": ["P", "C1'", "P", "C1'"], "index": [0, 0, 1, 1]},
    "v0": {"atoms": ["C4'", "O4'", "C1'", "C2'"], "index": [0, 0, 0, 0]},
    "v1": {"atoms": ["O4'", "C1'", "C2'", "C3'"], "index": [0, 0, 0, 0]},
    "v2": {"atoms": ["C1'", "C2'", "C3'", "C4'"], "index": [0, 0, 0, 0]},
    "v3": {"atoms": ["C2'", "C3'", "C4'", "O4'"], "index": [0, 0, 0, 0]},
    "v4": {"atoms": ["C3'", "C4'", "O4'", "C1'"], "index": [0, 0, 0, 0]},
}
