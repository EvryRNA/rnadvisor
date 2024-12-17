import transformers
from transformers import AutoModel, AutoTokenizer
import numpy as np
import pandas as pd
from typing import Optional, Dict
import os
os.environ["TOKENIZERS_PARALLELISM"]="false"

model_name = "sayby/rna_torsionBERT"
tokenizer = AutoTokenizer.from_pretrained(
    model_name, trust_remote_code=True
)
params_tokenizer = {
    "return_tensors": "pt",
    "padding": "max_length",
    "max_length": 512,
    "truncation": True,
}
model = AutoModel.from_pretrained(
    model_name, trust_remote_code=True
)
