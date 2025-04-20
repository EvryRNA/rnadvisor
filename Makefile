REMOTE_PATH=/nhome/siniac/cbernard/Documents/these/project/evry_rna/sf_official

local_to_remote:
	rsync -ovapx --exclude='.git' --exclude='.idea' --exclude='*__pycache__*' --exclude=".venv"  \
			--exclude='tmp' . local_gpu:$(REMOTE_PATH)/

load_data:
	rsync -ovapx local_gpu:$(REMOTE_PATH)/data/output/top_50k_synthetic_clash.csv ./data/output/

NATIVE_PATH=data/input/PREDS/R1107/R1107.pdb
PRED_DIR=data/input/PREDS/R1107
OUT_DIR=data/output/scores
OUT_TIME_DIR=data/output/times

build_rnabriq:
	docker compose build rna_briq
	docker compose run --rm rna_briq

build_lcs:
	docker compose build lcs
	docker compose run --rm lcs --native_path=data/example/NATIVE/R1107.pdb --pred_dir=data/example/PREDS \
		--out_path=data/output/scores/lcs/R1107.csv --out_time_path=data/output/times/lcs/time_R1107.csv \
		 --params='{"mcq_threshold": [10, 15], "mcq_mode": 2}'

#PRED_DIR=data/input/RNA_PUZZLES_DECOYS/PREDS/rp08
#NATIVE_PATH=data/input/RNA_PUZZLES_DECOYS/PREDS/rp08/rp08.pdb

run_rnadvisor:
	uv run rnadvisor --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=data/output/all_scores/R1107.csv --out_time_path=data/output/all_scores/time_R1107.csv \
		--scores=rmsd,inf,mcq,rasp --params='{"mcq_threshold": [10, 15, 20, 25], "mcq_mode": 2}' \
		--verbose=2 --z_score

run_ares:
	uv run rnadvisor --pred_dir=../pcc/data/input/RNA_PUZZLES_DECOYS/PREDS/rp14_free/ \
	--out_path=../pcc/data/tmp/ares/RNA_PUZZLES_DECOYS/rp14_free.csv --scores=ares

run_cif:
	uv run rnadvisor --pred_dir=data/input/CIF --out_path=out.csv --scores=3drnascore --normalise