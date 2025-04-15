FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including Python 3.10 and pip
RUN apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    cmake \
    make \
    g++ \
    curl \
    ca-certificates \
    && add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && apt-get install -y \
    python3.10 \
    python3.10-distutils \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    ln -s /usr/bin/python3.10 /usr/bin/python && \
    ln -s /usr/local/bin/pip /usr/bin/pip && \
    rm -rf /var/lib/apt/lists/*

# Install Voronota
WORKDIR /opt
RUN wget https://github.com/kliment-olechnovic/voronota/releases/download/v1.29.4370/voronota_1.29.4370.tar.gz && \
    tar -xf voronota_1.29.4370.tar.gz

WORKDIR /opt/voronota_1.29.4370
RUN cmake . -DEXPANSION_JS=ON -DEXPANSION_LT=ON && \
    make && \
    make install

# Install Python dependencies
COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

# Copy application code
COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

WORKDIR /app

ENTRYPOINT ["python3", "-m", "rnadvisor.metric.voronota.cad_score_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]
