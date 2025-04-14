FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-distutils \
    git \
    build-essential \
    gfortran \
    libhdf5-dev \
    libnetcdf-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p lib/barnaba && \
    git clone --branch scoring-version3.8 https://github.com/clementbernardd/barnaba.git lib/barnaba

RUN pip install --no-cache-dir -r lib/barnaba/requirements.txt
CMD ["/bin/bash"]

#RUN pip install --upgrade pip setuptools wheel
#RUN pip install lz4==4.3.2
#RUN pip install "numpy==1.17.3" --no-binary=:all:


#COPY src/rnadvisor /app/rnadvisor
#COPY data/example /app/data/example
#
#ENTRYPOINT ["python", "-m", "rnadvisor.metric.barnaba.barnaba_helper"]
#CMD ["--pred_dir=data/example/PREDS"]
