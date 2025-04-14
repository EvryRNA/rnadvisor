NATIVE_PATH := "data/input/NATIVE/R1107.pdb"
PRED_DIR := "data/input/PREDS/R1107"
OUT_DIR := "data/output/scores"
OUT_TIME_DIR := "data/output/times"

build-full IMAGE:
	docker compose -f docker-compose.yaml build {{IMAGE}}

build-slim IMAGE EXEC_PATH TAG:
	docker-slim build \
	  --target {{IMAGE}} \
	  --tag {{TAG}} \
	  --http-probe=false \
	  --continue-after=exec \
	  --include-path /usr/local/lib/python3.10/site-packages/torch/bin/torch_shm_manager \
	  --include-path /usr/local/lib/python3.7/site-packages/torch/bin/torch_shm_manager \
	  --exec "python -m {{EXEC_PATH}} --pred_dir=data/example/PREDS --native_path=data/example/NATIVE/R1107.pdb"

run-slim SERVICE EXEC_NAME:
	docker compose -f docker-compose.slim.yaml run --rm {{SERVICE}} \
	  --native_path={{NATIVE_PATH}} \
	  --pred_dir={{PRED_DIR}} \
	  --out_path={{OUT_DIR}}/{{EXEC_NAME}}/R1107.csv \
	  --out_time_path={{OUT_TIME_DIR}}/{{EXEC_NAME}}/R1107.csv

build-3drnascore-full:
	just build-full "3drnascore"

build-3drnascore-slim: build-3drnascore-full
	just build-slim "3drnascore_image" "rnadvisor.scoring_function.rnascore.rnascore_helper" "3drnascore_slim"

run-3drnascore-slim:
	just run-slim "3drnascore" "3drnascore"

build-lociparse-full:
	just build-full "lociparse"

build-lociparse-slim: build-lociparse-full
	just build-slim "lociparse_image" "rnadvisor.scoring_function.lociparse.lociparse_helper" "lociparse_slim"

run-lociparse-slim:
	just run-slim "lociparse" "lociparse"

build-tb_mcq-full:
	just build-full "tb_mcq"

build-tb_mcq-slim: build-tb_mcq-full
	just build-slim "tb_mcq_image" "rnadvisor.scoring_function.tb_mcq.tb_mcq_helper" "tb_mcq_slim"

run-tbmcq-slim:
	just run-slim "tb_mcq" "tb_mcq"

build-clash-full:
	just build-full "clash"

build-clash-slim: build-clash-full
	just build-slim "clash_image" "rnadvisor.scoring_function.clash.clash_helper" "clash_slim"

run-clash-slim:
	just run-slim "clash" "clash"

build-pamnet-full:
	just build-full "pamnet"

build-pamnet-slim: build-pamnet-full
	just build-slim "pamnet_image" "rnadvisor.scoring_function.pamnet.pamnet_helper" "pamnet_slim"

run-pamnet-slim:
	just run-slim "pamnet" "pamnet"

build-barnaba-full:
	just build-full "barnaba"

build-barnaba-slim: build-barnaba-full
	just build-slim "barnaba_image" "rnadvisor.metric.barnaba.barnaba_helper" "barnaba_slim"

run-barnaba-slim:
	just run-slim "barnaba" "barnaba"

build-cgrnasp-full:
	just build-full "cgrnasp"

build-cgrnasp-slim: build-cgrnasp-full
	just build-slim "cgrnasp_image" "rnadvisor.scoring_function.cgrnasp.cgrnasp_helper" "cgrnasp_slim"

run-cgrnasp-slim:
	just run-slim "cgrnasp" "cgrnasp"

build-dfire-full:
	just build-full "dfire"

build-dfire-slim: build-dfire-full
	just build-slim "dfire_image" "rnadvisor.scoring_function.dfire.dfire_helper" "dfire_slim"

run-dfire-slim:
	just run-slim "dfire" "dfire"

build-mcq-full:
	just build-full "mcq"

build-mcq-slim: build-mcq-full
	just build-slim "mcq_image" "rnadvisor.metric.mcq4structures.mcq_helper" "mcq_slim"

run-mcq-slim:
	just run-slim "mcq" "mcq"

build-lcs-full:
	just build-full "lcs"

build-lcs-slim: build-lcs-full
	just build-slim "lcs_image" "rnadvisor.metric.mcq4structures.lcs_helper" "lcs_slim"

run-lcs-slim:
	just run-slim "lcs" "lcs"
