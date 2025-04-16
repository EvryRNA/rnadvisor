FROM python:3.10-slim

WORKDIR /app

COPY requirements/lociparse-requirements.txt lociparse.txt
COPY requirements/wrapper-requirements.txt wrapper.txt
RUN cat wrapper.txt lociparse.txt > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

ENTRYPOINT ["python", "-m", "rnadvisor.scoring_function.lociparse.lociparse_helper"]
CMD ["--pred_dir=data/example/PREDS"]
