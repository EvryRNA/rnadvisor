![img](img/RNAdvisor_page.gif)

<div align="center">

<!-- omit in toc -->
# RNAdvisor v2 🚀
<strong>Fast and easy way to compute RNA 3D structural quality</strong>

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![slim](https://img.shields.io/badge/docker-slim-blue)](https://github.com/slimtoolkit/slim)
[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg)](https://badge.fury.io/py/tensorflow)
[![DOI](https://img.shields.io/badge/DOI-10.1093/bib/bbae064-green)](https://doi.org/10.1093/bib/bbae064)

</div>

RNAdvisor is a wrapper tool for the computation of RNA 3D structural quality assessment. 
It uses [docker compose](https://docs.docker.com/compose/) to run the RNAdvisor tool in a containerized environment. 

```python
from rnadvisor.rnadvisor_cli import RNAdvisorCLI

rnadvisor_cli = RNAdvisorCLI(
    pred_dir="data/example/PREDS",
    native_path="data/example/NATIVE/R1107.pdb",
    out_path="out.csv",
    scores=["rmsd", "inf", "mcq", "lddt","tm-score", "gdt-ts", "ares", "pamnet"]
)
df_results, df_time = rnadvisor_cli.predict()
```

![img](img/RNAdvisor-screencast.gif)


## Installation

To install RNAdvisor v2 you need to have [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) installed on your system.
Then, you can install the package using pip:

```bash
pip install rnadvisor
```

Then you can compute the RNA 3D structural quality assessment using the command line interface (CLI) or the python API.
```bash
rnadvisor --pred_dir --scores [--native_path] [--out_path ]
          [--out_time_path] [--sort_by] [--params] [--tmp_dir] 
          [--verbose] [--z_score] [--normalise]
``` 
with: 
```
  --pred_dir            Directory to .pdb files or path to a .pdb file of the predictions. 
  --native_path         Path to a .pdb file of the native structure.
  --scores              List of the scores to use, separated by a comma. 
                        If you want to use them all, use `all`. To use all the metrics, use `metrics`
                        To use all the scoring functions, use `sf`.
                        Choice between clash,pamnet,lociparse,3drnascore,tb-mcq,barnaba,cgrnasp,dfire,mcq,
                        lcs,cad-score,tm-score,lddt,rasp,rs-rnasp,rmsd,inf,p-value,di,gdt-ts,ares
  --out_path            Path to a .csv file where to save the predictions.
  --out_time_path       Path to a .csv file where to save the time of the predictions for each score.
  --sort_by             Metric to sort the results by.
  --verbose             Level of verbosity. 0 for no output, 1 for basic output, 2 for detailed output.
  --params              Hyperparameters of the different methods. It could be used to set the threshold for LCS-TA 
   or parameters of MCQ using `--params='{"mcq_threshold": 10, "mcq_mode": 2}'`. Values for `mcq_threshold` are 10, 15, 20 or 25 and values for 
    `mcq_mode` are 0 (relaxed), 1 (comparison without violations) or 2 (comparison of everything regardless violations).
  --z_score             Compute the Z-score for the computed scores. It reverses all the descreasing scores.
  --normalise           If the user doesn't want to normalise the .pdb files. It will run the --rna-puzzles-ready from RNA-tools.
  --sort-by             Metric to sort the results by. Choice between RMSD,P-VALUE,INF-ALL,INF-WC,INF-NWC,INF-STACK,DI,MCQ,TM-SCORE,GDT-TS,GDT-TS@1,GDT-TS@2,GDT-TS@4,GDT-TS@8,CAD,lDDT,RASP,BARNABA,DFIRE,rsRNASP.
```

## Existing tools

This code implements 18 existing repositories and adds a python interface. 

It takes as inputs a `.pdb` file of predicted 3D structures (or a folder of `.pdb` files) and a 
`.pdb` file of a native structure, and it returns a `.csv` file with the different metrics. 

It uses the following repositories: 

- [RNA_Assessment](https://github.com/RNA-Puzzles/RNA_assessment): a python repository that computes [RMSD](#rmsd), [P-VALUE](#p-value), [INF](#inf), and [DI](#di). 
    I forked the project because I did some modifications, leading to use the following implementation of [RNA_Assessment-forked](https://github.com/clementbernardd/RNA_assessment/tree/scoring-version)
- [MCQ4Structures](https://github.com/tzok/mcq4structures) : a java code that computes the [MCQ](#mcq) score. 
- [Voronota](https://github.com/kliment-olechnovic/voronota): a C++ code that computes the [CAD](#cad) score. 
- [Zhanglab](https://zhanggroup.org/TM-score/): a complete website to compute multiple scores, such as the [GDT-TS](#gdt-ts) or [TM-score](#tm-score) scores.
- [BaRNAba](https://github.com/srnas/barnaba): an implementation of the eRMSD and eSCORE. I created a fork version of [BaRNAba-forked](https://github.com/clementbernardd/barnaba/tree/scoring-version).
- [DFIRE](https://github.com/tcgriffith/dfire_rna): an implementation of the DFIRE energy function. 
- [RASP](http://melolab.org/webrasp/download.php): an implementation of the RASP energy function. I created a fork version of [RASP-forked](https://github.com/clementbernardd/rasp_rna)
- [rsRNASP](https://github.com/Tan-group/rsRNASP): a Python implementation of the rsRNASP score. I created a fork version of [rsRNASP-forked](https://github.com/clementbernardd/rsRNASP/tree/scoring-version) with only the needed files.
- [cgRNASP](https://github.com/Tan-group/cgRNASP): a Python implementation of the cgRNASP score. 
- [OpenStructure](https://git.scicore.unibas.ch/schwede/openstructure): a C++ and Python implementation for structure analysis. It is used to compute [TM-score](#tm-score) and [lDDT]($lddt) metrics. 
- [CGRNASP](https://github.com/Tan-group/cgRNASP): a C implementation for the computation of CG-RNASP potentials. I created a fork version of [CGRNASP-forked](https://github.com/clementbernardd/cgrnasp_fork.git). 
- [TB-MCQ](https://github.com/EvryRNA/RNA-TorsionBERT): a python implementation of the TB-MCQ score. It uses predicted torsional angles from a language-based model to compute the MCQ score with the inferred angles from a given structure.
- [ARES](https://www.science.org/doi/10.1126/science.abe5650): an implementation of ARES. I'm using a docker container derived from `adamczykb/ares_qa` that I have reduced. I also added inside the [`reduce`](https://github.com/rlabduke/reduce) repository to add hydrogens to make ARES works.
- [PAMNet](https://github.com/XieResearchGroup/Physics-aware-Multiplex-GNN): official implementation of PAMNet. I have reduced the docker image to only keep the necessary files to run the scoring function.
- [CLASH](https://github.com/mantczak/rnaqua): RESTful web service client developed in Java that enables the computation of the CLASH score. 
- [LociPARSE](https://github.com/Bhattacharya-Lab/lociPARSE): official python implementation of LociPARSE.
- [RNA3DCNN](https://github.com/lijunRNA/RNA3DCNN): official python implementation of RNA3DCNN. I have reduced to a docker image that only works with GPU.
- [3dRNAScore](http://biophy.hust.edu.cn/new/resources/3dRNAscore): C++ official implementation of the 3dRNAScore.

Note that all these repositories are implementing a lot of different functions. 
For the sake of this project, I just took what seemed to be the most relevant for the scoring of 3D structures. 


## Docker containers

Each of the scoring functions and metrics are isolated in individual docker containers.
You can find each of them in dockerhub with: `sayby/rnadvisor-<name>-slim` or `sayby/rnadvisor-<name>`.

`<name>` can be one of the following:

| Scoring Function | Metric      |
|------------------|-------------|
| `3drnascore`     | `rmsd`      |
| `lociparse`      | `inf`       |
| `tb-mcq`         | `p-value`   |
| `escore`         | `di`        |
| `pamnet`         | `mcq`       |
| `cgrnasp`        | `gdt-ts`    |
| `dfire`          | `lddt`      |
| `rasp`           | `tm-score`  |
| `rsRNASP`        | `cad-score` |
| `ares`            | `clash`         |


The `slim` version is a smaller version of the container that only contains the necessary codes to run the scoring function (e.g. no bash, no other commands, etc.).
It corresponds to the original image reduced with [`docker-slim`](https://github.com/slimtoolkit/slim).

## Docker build

If you want to build yourself the docker images, you can do so by running the following command in the root directory of the repository:

```bash
just build-<name>-full 
```
with `<name>` being the name of the scoring function/metric you want to build.

To get the `slim` version, you can run the following command:

```bash
just build-<name>-slim
```

## Citation 
```
Clement Bernard, Guillaume Postic, Sahar Ghannay, Fariza Tahi,
RNAdvisor: a comprehensive benchmarking tool for the measure and prediction of RNA structural model quality,
Briefings in Bioinformatics, Volume 25, Issue 2, March 2024, bbae064,
https://doi.org/10.1093/bib/bbae064
```