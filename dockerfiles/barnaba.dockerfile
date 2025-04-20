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
COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

RUN find /usr/local/lib/python3.8/site-packages/ -name '*nspkg.pth' -exec rm -v {} +

ENTRYPOINT ["python", "-m", "rnadvisor.metric.barnaba.barnaba_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]
