# Build stage for the RNA_Assessment
FROM python:3.8 as rna_assessment
WORKDIR /src/
COPY Makefile .
RUN make install_rna_assessment # Git clone RNA_Assessment fork, a pyton code

FROM maven:3.8.7-openjdk-18-slim AS mcq_dependencies
WORKDIR /app
RUN apt-get update && apt-get install -y git
RUN mkdir lib && git clone https://github.com/tzok/mcq4structures.git ./lib/mcq4structures
RUN mvn -B package --file lib/mcq4structures/pom.xml

FROM maven:3.8.7-openjdk-18-slim AS mcq_builder
WORKDIR /app
COPY --from=mcq_dependencies /root/.m2 /root/.m2
COPY --from=mcq_dependencies /app/ /app/
RUN mvn -B -e clean install --file lib/mcq4structures/pom.xml


# Build stage for the Zhanglab group : a C++ based code
FROM gcc:9.5.0 AS zhanglab
WORKDIR /src/
COPY Makefile .
# Download the TMScore.cpp file and build the binary file
RUN make install_zhanggroup && \
    make build_tm


FROM python:3.8 as barnaba
# Image not used as this is just a python code
WORKDIR /src
COPY Makefile .
RUN make install_barnaba

FROM registry.scicore.unibas.ch/schwede/openstructure as ares
WORKDIR /app/
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y software-properties-common git && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.8 python3-pip python3.8-dev python3.8-venv
RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH
RUN pip3 install --upgrade pip
# Download ARES codes
RUN git clone https://github.com/clementbernardd/ares_fork.git --branch scoring .
RUN pip3 install -r requirements.txt
RUN pip3 install -r post_requirements.txt
RUN pip3 install torch-scatter==2.0.5 -f https://pytorch-geometric.com/whl/torch-1.5.0+cu102.html


# Final stage for the scoring process, using the previous build stages
FROM registry.scicore.unibas.ch/schwede/openstructure as release
WORKDIR /app/
# Copy python requirements - couldn't build an image as this is interpreted
COPY requirements.txt .
# Copy the python code from RNA_Assessment and MC-Annotate binary file
COPY --from=rna_assessment /src/lib/rna_assessment ./lib/rna_assessment
COPY --from=zhanglab /src/lib/zhanggroup/ ./lib/zhanggroup
COPY --from=mcq_builder /app/lib/mcq4structures/*.jar /app/lib/mcq4structures/app.jar
COPY --from=mcq_builder /app/lib/mcq4structures /app/lib/mcq4structures

ENV RASP=/app/lib/rasp
ENV DFIRE_RNA_HOME=/app/lib/dfire
ENV JAVA_HOME='/opt/jdk-17'
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV PATH=/venv/bin:$PATH
RUN apt-get update &&\
    apt-get install -y --no-install-recommends make git software-properties-common
COPY Makefile .
RUN make install_dfire
RUN cd lib/dfire ; make
RUN make install_rasp
RUN cd lib/rasp ; make rna
RUN make install_rs_rnasp
RUN cd lib/rs_rnasp ; make build
RUN make install_barnaba
RUN make install_cg_rnasp
RUN make install_usalign
RUN pip install --no-cache-dir -r requirements.txt
RUN ulimit -c unlimited # To enable MCQ4structures to run well
RUN echo "" > lib/__init__.py
# Install Java
ENV JAVA_VERSION=18 \
    JAVA_HOME=/usr/lib/jvm/java-18-openjdk-amd64
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common && \
    wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && \
    add-apt-repository -y https://packages.adoptium.net/artifactory/deb && \
    apt-get update && \
    apt-get install -y openjdk-18-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
# Add pytorch CPU
RUN pip install torch==2.2.0+cpu torchvision==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
COPY . .
RUN python3 tests/test_tf.py # To download the model weights for TB-MCQ
CMD /bin/bash


FROM release as dev
RUN apt-get update && apt-get install -y bc vim
ENTRYPOINT ["/bin/bash"]
