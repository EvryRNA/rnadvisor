import os

from transformers import AutoModel, AutoTokenizer


def download_model(model_path, model_name):
    """Download a Hugging Face model and tokenizer to the specified directory"""
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True).cpu()

    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)


download_model("models/sayby_rna_torsionbert", "sayby/rna_torsionbert")
