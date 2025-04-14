FROM python:3.7.4-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    liblzma-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

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

RUN git clone https://github.com/clementbernardd/Physics-aware-Multiplex-GNN.git --branch dev pamnet

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.pamnet.pamnet_helper"]
CMD ["--pred_dir=data/example/PREDS"]