NATIVE_PATH := "data/input/NATIVE/R1107.pdb"
PRED_DIR := "data/input/PREDS/R1107"
OUT_DIR := "data/output/scores"
OUT_TIME_DIR := "data/output/times"

build-full IMAGE:
	docker compose -f docker-compose.yaml build {{IMAGE}}

build-slim IMAGE EXEC_PATH TAG:
	docker-slim build \
	  --target {{IMAGE}} \
	  --tag "sayby77/rnadvisor-"{{TAG}} \
	  --http-probe=false \
	  --continue-after=exec \
	  --include-path /usr/local/lib/python3.10/site-packages/torch/bin/torch_shm_manager \
	  --include-path /usr/local/lib/python3.7/site-packages/torch/bin/torch_shm_manager \
	  --exec "python3 -m {{EXEC_PATH}} --pred_dir=data/example/PREDS --native_path=data/example/NATIVE/R1107.pdb --params='{\"mcq_threshold\": 15, \"mcq_mode\": 2}'"

run-slim SERVICE EXEC_NAME:
	docker compose -f src/docker-compose.slim.yaml run --rm {{SERVICE}} \
	  --native_path={{NATIVE_PATH}} \
	  --pred_dir={{PRED_DIR}} \
	  --out_path={{OUT_DIR}}/{{EXEC_NAME}}/R1107.csv \
	  --out_time_path={{OUT_TIME_DIR}}/{{EXEC_NAME}}/R1107.csv

build-3drnascore-full:
	just build-full "3drnascore"

build-3drnascore-slim: build-3drnascore-full
	just build-slim "3drnascore_image" "rnadvisor.scoring_function.rnascore.rnascore_helper" "3drnascore-slim"

run-3drnascore-slim:
	just run-slim "3drnascore" "3drnascore"

build-lociparse-full:
	just build-full "lociparse"

build-lociparse-slim: build-lociparse-full
	just build-slim "lociparse_image" "rnadvisor.scoring_function.lociparse.lociparse_helper" "lociparse-slim"

run-lociparse-slim:
	just run-slim "lociparse" "lociparse"

build-tb_mcq-full:
	just build-full "tb_mcq"

build-tb_mcq-slim: build-tb_mcq-full
	just build-slim "tb_mcq_image" "rnadvisor.scoring_function.tb_mcq.tb_mcq_helper" "tb-mcq-slim"

run-tbmcq-slim:
	just run-slim "tb_mcq" "tb_mcq"

build-clash-full:
	just build-full "clash"

build-clash-slim: build-clash-full
	just build-slim "clash_image" "rnadvisor.scoring_function.clash.clash_helper" "clash-slim"

run-clash-slim:
	just run-slim "clash" "clash"

build-pamnet-full:
	just build-full "pamnet"

build-pamnet-slim: build-pamnet-full
	just build-slim "pamnet_image" "rnadvisor.scoring_function.pamnet.pamnet_helper" "pamnet-slim"

run-pamnet-slim:
	just run-slim "pamnet" "pamnet"

build-barnaba-full:
	just build-full "barnaba"

build-barnaba-slim: build-barnaba-full
	just build-slim "barnaba_image" "rnadvisor.metric.barnaba.barnaba_helper" "barnaba-slim"

run-barnaba-slim:
	just run-slim "barnaba" "barnaba"

build-cgrnasp-full:
	just build-full "cgrnasp"

build-cgrnasp-slim: build-cgrnasp-full
	just build-slim "cgrnasp_image" "rnadvisor.scoring_function.cgrnasp.cgrnasp_helper" "cgrnasp-slim"

run-cgrnasp-slim:
	just run-slim "cgrnasp" "cgrnasp"

build-dfire-full:
	just build-full "dfire"

build-dfire-slim: build-dfire-full
	just build-slim "dfire_image" "rnadvisor.scoring_function.dfire.dfire_helper" "dfire-slim"

run-dfire-slim:
	just run-slim "dfire" "dfire"

build-mcq-full:
	just build-full "mcq"

build-mcq-slim: build-mcq-full
	just build-slim "mcq_image" "rnadvisor.metric.mcq4structures.mcq_helper" "mcq-slim"

run-mcq-slim:
	just run-slim "mcq" "mcq"

build-lcs-full:
	just build-full "lcs"

build-lcs-slim: build-lcs-full
	just build-slim "lcs_image" "rnadvisor.metric.mcq4structures.lcs_helper" "lcs-slim"

run-lcs-slim:
	just run-slim "lcs" "lcs"

build-lddt-full:
	just build-full "lddt"

build-lddt-slim: build-lddt-full
	just build-slim "lddt_image" "rnadvisor.metric.open_structures.lddt_helper" "lddt-slim"

run-lddt-slim:
	just run-slim "lddt" "lddt"

build-rasp-full:
	just build-full "rasp"

build-rasp-slim: build-rasp-full
	just build-slim "rasp_image" "rnadvisor.scoring_function.rasp.rasp_helper" "rasp-slim"

run-rasp-slim:
	just run-slim "rasp" "rasp"

build-rs_rnasp-full:
	just build-full "rs_rnasp"

build-rs_rnasp-slim: build-rasp-full
	just build-slim "rs_rnasp_image" "rnadvisor.scoring_function.rs_rnasp.rs_rnasp_helper" "rs-rnasp-slim"

run-rs_rnasp-slim:
	just run-slim "rs_rnasp" "rs_rnasp"

build-rmsd-full:
	just build-full "rmsd"

build-rmsd-slim: build-rmsd-full
	just build-slim "rmsd_image" "rnadvisor.metric.rna_assessment.rmsd_helper" "rmsd-slim"

run-rmsd-slim:
	just run-slim "rmsd" "rmsd"

build-inf-full:
	just build-full "inf"

build-inf-slim: build-inf-full
	just build-slim "inf_image" "rnadvisor.metric.rna_assessment.inf_helper" "inf-slim"

run-inf-slim:
	just run-slim "inf" "inf"

build-di-full:
	just build-full "di"

build-di-slim: build-di-full
	just build-slim "di_image" "rnadvisor.metric.rna_assessment.di_helper" "di-slim"

run-di-slim:
	just run-slim "di" "di"

build-p_value-full:
	just build-full "p_value"

build-p_value-slim: build-p_value-full
	just build-slim "p_value_image" "rnadvisor.metric.rna_assessment.p_value_helper" "p-value-slim"

run-p_value-slim:
	just run-slim "p_value" "p_value"

build-tm_score-full:
	just build-full "tm_score"

build-tm_score-slim: build-tm_score-full
	just build-slim "tm_score_image" "rnadvisor.metric.zhanggroup.tm_score_helper" "tm-score-slim"

run-tm_score-slim:
	just run-slim "tm_score" "tm_score"

build-cad_score-full:
	just build-full "cad_score"

build-cad_score-slim: build-cad_score-full
	just build-slim "cad_score_image" "rnadvisor.metric.voronota.cad_score_helper" "cad-score-slim"

run-cad_score-slim:
	just run-slim "cad_score" "cad_score"

build-gdt_ts-full:
	just build-full "gdt_ts"

build-gdt_ts-slim: build-gdt_ts-full
	just build-slim "gdt_ts_image" "rnadvisor.metric.zhanggroup.gdt_ts_helper" "gdt-ts-slim"

run-gdt_ts-slim:
	just run-slim "gdt_ts" "gdt_ts"

build-ares-full:
	just build-full "ares"

build-ares-slim: build-ares-full
	just build-slim "ares_image" "rnadvisor.scoring_function.ares.ares_helper" "ares-slim"

run-ares-slim:
	just run-slim "ares" "ares"

build-rna3dcnn-full:
	just build-full "rna3dcnn"

build-rna3dcnn-slim: build-rna3dcnn-full
	just build-slim "rna3dcnn_image" "rnadvisor.scoring_function.rna3dcnn.rna3dcnn_helper" "rna3dcnn-slim"

run-rna3dcnn-slim:
	just run-slim "rna3dcnn" "rna3dcnn"

build-rna_briq-full:
	just build-full "rna_briq"

build-rna_briq-slim: build-rna_briq-full
	just build-slim "rna_briq_image" "rnadvisor.scoring_function.rna_briq.rna_briq_helper" "rna-briq-slim"

run-rna_briq-slim:
	just run-slim "rna_briq" "rna_briq"
