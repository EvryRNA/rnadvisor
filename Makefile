# Path to check the code
export PATH_TO_CODE=src
# Path to the unit tests
export PATH_TO_UNIT_TESTS=tests/unit

# Score thresholds
export COVERAGE_SCORE=35
export COMPLEXITY_SCORE=3
export DOCUMENTATION_SCORE=5

# Max line length for black
MAX_LINE_LENGTH=99
export PYTHON?=python3 -m

# Path to the lintage directory
LINTAGE_DIR=script/lintage

# Convert the code to black format
format_code :
	$(PYTHON) black --line-length $(MAX_LINE_LENGTH) ${PATH_TO_CODE}

# Do all the static tests
test_static_all: format_code
	$(PYTHON) black --check --line-length $(MAX_LINE_LENGTH)  ${PATH_TO_CODE}
	$(PYTHON) isort --profile black ${PATH_TO_CODE}
	$(PYTHON) mypy ${PATH_TO_CODE} --ignore-missing-imports
	$(PYTHON) flake8 --exclude=tests,src/rna_tools --max-line-length $(MAX_LINE_LENGTH) ${PATH_TO_CODE}

# Unit tests
unit_test:
	$(PYTHON) pytest ${PATH_TO_UNIT_TESTS}

test_unit_coverage:
	${LINTAGE_DIR}/coverage.sh

test_complexity:
	${LINTAGE_DIR}/complexity.sh

test_documentation:
	${LINTAGE_DIR}/documentation.sh

all_tests: test_static_all test_complexity test_documentation test_unit_coverage

.PHONY: compute_scores
compute_scores:
	$(PYTHON) src.rnadvisor_cli --config_path=./config.yaml

.PHONY: docker_start
docker_start:
	docker build -t rnadvisor --target release .
	docker run --rm -it -v ${PWD}/docker_data/:/app/docker_data -v ${PWD}/tmp:/app/tmp -v ${PWD}/config.yaml:/app/config.yaml rnadvisor --config_path=./config.yaml

.PHONY: docker_interactive
docker_interactive:
	docker build -t rnadvisor_dev --target dev .
	docker run --rm -it -v ${PWD}/docker_data/:/app/docker_data -v ${PWD}/tmp:/tmp -v ${PWD}/config.yaml:/app/config.yaml rnadvisor_dev

.PHONY: clean
clean:
	if [ -d "tmp" ]; then rm -r tmp; fi

build_all: build_tm install_mcq

##################################################################################################
################ Code from the Zhangroup to get GDT-TS score ###################
##################################################################################################

# Command to build the C++ code for the TM-scores and GDT_TS scores
CC=g++
CFLAGS=-static -O3 -ffast-math -lm
SRC1=lib/zhanggroup/TMscore.cpp
EXE1=lib/zhanggroup/TMscore

build_tm: $(EXE1)

$(EXE1): $(SRC1)
	$(CC) $(SRC1) $(CFLAGS) -o $(EXE1)

.PHONY: install_zhanggroup
install_zhanggroup:
	mkdir -p lib/zhanggroup
	wget -O ./lib/zhanggroup/TMscore.cpp https://zhanggroup.org/TM-score/TMscore.cpp

##################################################################################################
#################### Code from the RNA_Assessment to compute : ###################################
############################ RMSD, P-VALUE, INF and DI ###########################################
##################################################################################################

.PHONY: install_rna_assessment
install_rna_assessment:
	git clone https://github.com/clementbernardd/RNA_assessment.git --branch scoring-version ./lib/rna_assessment

##################################################################################################
#################### Code from the mcq4structures to compute the MCQ score #######################
##################################################################################################

.PHONY: install_mcq
install_mcq:
	git clone https://github.com/tzok/mcq4structures.git ./lib/mcq4structures
	mvn -B package --file lib/mcq4structures/pom.xml

.PHONY: example_mcq
example_mcq:
	lib/mcq4structures/mcq-cli/mcq-local -t data/NATIVE/1Z43.pdb -d tmp data/MODEL_2/FARFAR2-1Z43-S_000001_012_0001.pdb | awk '{print ${NF}}'

##################################################################################################
####################### Code from the voronota to compute the CAD score ##########################
##################################################################################################

.PHONY: example_cad
example_cad:
	voronota-cadscore --input-target data/NATIVE/1Z43.pdb --input-model data/MODEL_1/3dRNA-1Z43-7.pdb | awk '{print $5}'

##################################################################################################
################################## Code for RASP #################################################
##################################################################################################

.PHONY: install_rasp
install_rasp:
	mkdir -p lib/rasp
	git clone https://github.com/clementbernardd/rasp_rna --branch scoring-version lib/rasp/

##################################################################################################
################################## Code for barnaba ##############################################
##################################################################################################

.PHONY: install_barnaba
install_barnaba:
	mkdir -p lib/barnaba
	git clone https://github.com/clementbernardd/barnaba.git --branch scoring-version3.8 lib/barnaba
	pip install -r lib/barnaba/requirements.txt

##################################################################################################
################################# Code for DFIRE-RNA #############################################
##################################################################################################

.PHONY: install_difre
install_dfire:
	mkdir -p lib/dfire
	git clone https://github.com/tcgriffith/dfire_rna.git lib/dfire

##################################################################################################
################################## Code for rsRNASP ##############################################
##################################################################################################

.PHONY: install_rs_rnasp
install_rs_rnasp:
	mkdir -p lib/rs_rnasp
	git clone https://github.com/clementbernardd/rsRNASP.git --branch scoring-version lib/rs_rnasp

##################################################################################################
################################## Code for cgRNASP ##############################################
##################################################################################################

.PHONY: install_cg_rnasp
install_cg_rnasp:
	mkdir -p lib/cgRNASP
	git clone https://github.com/clementbernardd/cgrnasp_fork.git lib/cgRNASP
	make -C lib/cgRNASP install_all

