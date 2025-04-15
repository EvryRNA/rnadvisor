FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    make \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p lib/rs_rnasp && \
    git clone https://github.com/clementbernardd/rsRNASP.git --branch scoring-version lib/rs_rnasp && \
    cd lib/rs_rnasp ; make build

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.rs_rnasp.rs_rnasp_helper"]
CMD ["--pred_dir=data/example/PREDS"]