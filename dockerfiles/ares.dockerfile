FROM python:3.7.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    cmake \
    curl \
    sudo \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    liblzma-dev \
    libffi-dev \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root/build/reduce && \
    git clone https://github.com/rlabduke/reduce.git /root/src/reduce && \
    cd /root/build/reduce && \
    cmake /root/src/reduce && \
    make && \
    sudo make install

RUN pip install --upgrade pip setuptools wheel

RUN pip install \
    torch==1.8.0+cpu \
    torchvision==0.9.0+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html

COPY requirements/pamnet-requirements.txt pamnet.txt
COPY requirements/wrapper-requirements.txt wrapper.txt

RUN cat wrapper.txt pamnet.txt > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

RUN pip install \
    torch-scatter==2.0.7 \
    torch-sparse==0.6.12 \
    torch-cluster==1.5.9 \
    torch-geometric==1.7.2 \
    -f https://data.pyg.org/whl/torch-1.8.0+cpu.html

RUN wget https://zenodo.org/records/5090151/files/e3nn_ares.zip && \
    wget https://zenodo.org/records/6893040/files/ares_release.zip && \
    unzip e3nn_ares.zip && \
    unzip ares_release.zip && \
    rm *.zip && \
    mkdir -p lib/ares && \
    mv e3nn_ares ares_release lib/ares/

RUN pip install -e lib/ares/e3nn_ares
RUN pip install fsspec PyYAML tensorboard atom3d
RUN pip install pytorch_lightning==1.1.5


RUN find /usr/local/lib/python3.7/site-packages/ -name '*nspkg.pth' -exec rm -v {} +

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.ares.ares_helper"]
CMD ["--pred_dir=data/example/PREDS"]
