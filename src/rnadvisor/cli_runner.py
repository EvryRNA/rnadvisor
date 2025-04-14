import click
import json

def build_predict_cli(predictor_cls):
    @click.command()
    @click.option("--native_path", type=str, required=False, help="Path to the native structure (optional).")
    @click.option("--pred_dir", type=str, required=True, help="Path to the prediction directory or file of `.pdb` structures.")
    @click.option("--out_path", type=str, required=False, help="Path to a `.csv` file where to save the predictions.")
    @click.option("--out_time_path", type=str, required=False, help="Path to a `.csv` file where to save the time taken for each prediction.")
    @click.option('--quiet', is_flag=True, help='Suppress info logs')
    @click.option("--params", type=str, help="JSON string of parameters")
    def run(native_path, pred_dir, out_path, out_time_path, quiet, params):
        param_dict = json.loads(params) if params else {}
        predictor = predictor_cls(**param_dict, quiet=quiet)
        predictor.predict_dir(native_path, pred_dir, out_path, out_time_path)
    return run
