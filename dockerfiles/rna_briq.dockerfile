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

RUN git clone https://github.com/Jian-Zhan/RNA-BRiQ /app/RNA-BRiQ && \
    mkdir -p /app/RNA-BRiQ/build && \
    cd /app/RNA-BRiQ/build && \
    cmake ../ && make


COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
COPY tmp/rna-briq/BRiQ_data /app/BRiQ_data

ENV BRiQ_DATAPATH=/app/BRiQ_data
ENV PATH=$PATH:/app/RNA-BRiQ/build/bin

ENTRYPOINT ["/bin/bash"]
CMD []
