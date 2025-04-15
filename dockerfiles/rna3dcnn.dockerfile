FROM tensorflow/tensorflow:2.11.0-gpu

WORKDIR app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN git clone https://github.com/clementbernardd/RNA3DCNN.git --branch scoring_function .

RUN pip install biopython==1.78 pandas tqdm
COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt


COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.rna3dcnn.rna3dcnn_helper"]
CMD ["--pred_dir=data/example/PREDS"]