FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    make \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p lib/cgRNASP && \
    git clone https://github.com/clementbernardd/cgrnasp_fork.git lib/cgRNASP && \
    make -C lib/cgRNASP install_all

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.cgrnasp.cgrnasp_helper"]
CMD ["--pred_dir=data/example/PREDS"]
