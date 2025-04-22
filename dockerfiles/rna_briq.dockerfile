FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-distutils \
    git \
    build-essential \
    gfortran \
    cmake \
    libhdf5-dev \
    libnetcdf-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

ENV BRiQ_DATAPATH=/app/BRiQ_data
ENV PATH=$PATH:/app/RNA-BRiQ/build/bin

RUN git clone https://github.com/Jian-Zhan/RNA-BRiQ /app/RNA-BRiQ && \
    mkdir -p /app/RNA-BRiQ/build

COPY tmp/rna-briq/exec/ /app/RNA-BRiQ/exec

RUN cd /app/RNA-BRiQ/build && \
    cmake ../ && make -j $(nproc)

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
COPY tmp/rna-briq/BRiQ_data /app/BRiQ_data



ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.rna_briq.rna_briq_helper"]
CMD ["--pred_dir=data/example/PREDS"]
