FROM python:3.10-slim

WORKDIR /app

COPY requirements/tb_mcq-requirements.txt tb_mcq.txt
COPY requirements/wrapper-requirements.txt wrapper.txt
RUN cat wrapper.txt tb_mcq.txt > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/rnadvisor/scoring_function/tb_mcq/download_model.py /app/download_model.py

RUN python3 download_model.py

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.tb_mcq.tb_mcq_helper"]
CMD ["--pred_dir=data/example/PREDS"]
