FROM python:3.8-slim as rna_tools
WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    make \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p lib/rna_assessment && \
    git clone https://github.com/clementbernardd/RNA_assessment.git --branch scoring-version ./lib/rna_assessment

COPY requirements/wrapper-requirements.txt wrapper.txt
COPY requirements/rna_tools-requirements.txt rna_tools-requirements.txt
RUN cat wrapper.txt rna_tools-requirements.txt > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

FROM rna_tools as rmsd
ENTRYPOINT ["python", "-m", "rnadvisor.metric.rna_assessment.rmsd_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]

FROM rna_tools as inf
ENTRYPOINT ["python", "-m", "rnadvisor.metric.rna_assessment.inf_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]

FROM rna_tools as di
ENTRYPOINT ["python", "-m", "rnadvisor.metric.rna_assessment.di_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]

FROM rna_tools as p_value
ENTRYPOINT ["python", "-m", "rnadvisor.metric.rna_assessment.p_value_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]
