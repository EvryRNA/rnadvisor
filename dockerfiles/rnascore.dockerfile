FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    tar \
    make \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p lib/3drnascore && \
    wget -O lib/3drnascore/3dRNASCORE.tar.gz http://biophy.hust.edu.cn/new/downloads/3dRNASCORE.tar.gz && \
    tar -xvf lib/3drnascore/3dRNASCORE.tar.gz -C lib/3drnascore

ENV PYTHONPATH=/app/src

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.rnascore.rnascore_helper"]
CMD ["--pred_dir=data/example/PREDS"]
