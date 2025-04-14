FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    gcc \
    g++ \
    make \
    build-essential \
    libssl-dev \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/mantczak/rnaqua/releases/download/v1.1/rnaqua-binary.zip && \
    mkdir -p lib && \
    unzip rnaqua-binary.zip -d lib/rnaqua && \
    rm rnaqua-binary.zip && \
    chmod u+x lib/rnaqua/rnaqua-binary/bin/rnaqua.sh

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.clash.clash_helper"]
CMD ["--pred_dir=data/example/PREDS"]