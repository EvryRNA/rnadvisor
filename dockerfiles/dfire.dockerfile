FROM python:3.10-slim
ENV DFIRE_RNA_HOME=/app/lib/dfire

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    make \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p lib/dfire && \
    git clone https://github.com/tcgriffith/dfire_rna.git lib/dfire
RUN cd lib/dfire ; make

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.dfire.dfire_helper"]
CMD ["--pred_dir=data/example/PREDS"]