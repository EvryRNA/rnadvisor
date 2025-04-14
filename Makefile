REMOTE_PATH=/nhome/siniac/cbernard/Documents/these/project/evry_rna/sf_official

local_to_remote:
	rsync -ovapx --exclude='.git' --exclude='.idea' --exclude='*__pycache__*' --exclude=".venv"  \
			 . local_gpu:$(REMOTE_PATH)/

load_data:
	rsync -ovapx local_gpu:$(REMOTE_PATH)/data/output/top_50k_synthetic_clash.csv ./data/output/

NATIVE_PATH=data/input/NATIVE/R1107.pdb
PRED_DIR=data/input/PREDS/R1107
OUT_DIR=data/output/scores
OUT_TIME_DIR=data/output/times

build_tb_mcq:
	docker compose build tb_mcq
	docker compose run --rm tb_mcq --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=${OUT_DIR}/tb_mcq/R1107.csv --out_time_path=${OUT_TIME_DIR}/tb_mcq/R1107.csv

build_clash:
	docker compose build clash
	docker compose run --rm clash --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=${OUT_DIR}/clash/R1107.csv --out_time_path=${OUT_TIME_DIR}/clash/R1107.csv

build_pamnet:
	docker compose build pamnet
	docker compose run --rm pamnet --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=${OUT_DIR}/pamnet/R1107.csv --out_time_path=${OUT_TIME_DIR}/pamnet/R1107.csv
	#docker compose run --rm pamnet

build_barnaba:
	docker compose build barnaba
	docker compose run --rm barnaba --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=${OUT_DIR}/barnaba/R1107.csv --out_time_path=${OUT_TIME_DIR}/barnaba/R1107.csv

build_cgrnasp:
	docker compose build cgrnasp
	docker compose run --rm cgrnasp --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=${OUT_DIR}/cgrnasp/R1107.csv --out_time_path=${OUT_TIME_DIR}/cgrnasp/R1107.csv

build_dfire:
	docker compose build dfire
	docker compose run --rm dfire --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=${OUT_DIR}/dfire/R1107.csv --out_time_path=${OUT_TIME_DIR}/dfire/R1107.csv

build_mcq:
	docker compose build mcq
	docker compose run --rm mcq --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=${OUT_DIR}/mcq/R1107.csv --out_time_path=${OUT_TIME_DIR}/mcq/R1107.csv

build_lcs:
	docker compose build lcs
	docker compose run --rm lcs --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=${OUT_DIR}/lcs/R1107.csv --out_time_path=${OUT_TIME_DIR}/lcs/R1107.csv

run_rnadvisor:
	uv run rnadvisor --native_path=${NATIVE_PATH} --pred_dir=${PRED_DIR}\
		--out_path=data/output/all_scores/R1107.csv --out_time_path=data/output/all_scores/time_R1107.csv \
		--scores=clash,pamnet,lociparse,3drnascore,barnaba,cgrnasp,dfire,mcq,lcs,tb_mcq