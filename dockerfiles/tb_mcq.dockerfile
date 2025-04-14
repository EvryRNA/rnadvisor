FROM python:3.10-slim

WORKDIR /app

COPY requirements/tb_mcq-requirements.txt tb_mcq.txt
COPY requirements/wrapper-requirements.txt wrapper.txt

RUN cat wrapper.txt tb_mcq.txt > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('sayby/rna_torsionbert', trust_remote_code=True)"

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.tb_mcq.tb_mcq_helper"]
CMD ["--pred_dir=data/example/PREDS"]
