FROM maven:3.8.7-openjdk-18-slim AS mcq_dependencies
WORKDIR /app
RUN apt-get update && apt-get install -y git
RUN mkdir lib && git clone https://github.com/tzok/mcq4structures.git ./lib/mcq4structures
RUN mvn -B package --file lib/mcq4structures/pom.xml

# Stage 2: Build project
FROM maven:3.8.7-openjdk-18-slim AS mcq_builder
WORKDIR /app
COPY --from=mcq_dependencies /root/.m2 /root/.m2
COPY --from=mcq_dependencies /app/ /app/
RUN mvn -B -e clean install --file lib/mcq4structures/pom.xml


FROM python:3.10-slim AS mcq
WORKDIR /app

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

COPY --from=mcq_builder /app/lib/mcq4structures /app/lib/mcq4structures

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example
ENTRYPOINT ["python", "-m", "rnadvisor.metric.mcq4structures.mcq_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_dir=data.example/NATIVE/R1107.pdb"]