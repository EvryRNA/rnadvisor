FROM python:3.8
ENV LOCAL_PATH=.
WORKDIR app
COPY $LOCAL_PATH/pyproject.toml .
RUN apt-get update && apt-get install bc
RUN pip --no-cache-dir install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY $LOCAL_PATH .
