# Build stage for the RNA_Assessment
FROM python:3.8 as rna_assessment
WORKDIR /src/
COPY Makefile .
RUN make install_rna_assessment # Git clone RNA_Assessment fork, a pyton code

# Build stage for the MCQ4Structures : a java based code
FROM maven:3.9.0 AS mcq4structures
WORKDIR /src/
COPY Makefile .
# Clone the repo and install the dependencies using the pom.xml file
RUN apt-get update && apt-get install make
RUN make install_mcq

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
# Copy the codes for ARES
#COPY --from=ares /app/ ./lib/ares/
#COPY --from=ares /venv /venv

ENV RASP=/app/lib/rasp
ENV DFIRE_RNA_HOME=/app/lib/dfire
ENV JAVA_HOME='/opt/jdk-17'
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV PATH=/venv/bin:$PATH
# Install missing requirements
COPY Makefile .
RUN apt-get update &&\
    apt install maven -y  && \
    apt-get install -y --no-install-recommends default-jre-headless make git software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.8 python3-pip python3.8-dev python3.8-venv
RUN python3.8 -m venv /venv
RUN pip3 install --upgrade pip

RUN #pip install -e lib/ares/e3nn_ares
RUN pip install -r requirements.txt

RUN make install_dfire
RUN cd lib/dfire ; make
RUN make install_rasp
RUN cd lib/rasp ; make rna
RUN make install_rs_rnasp
RUN cd lib/rs_rnasp ; make build
RUN make install_barnaba
RUN make install_cg_rnasp
RUN make install_usalign
RUN apt-get install git-lfs &&\
    git lfs install && \
    make install_tb_mcq

RUN ulimit -c unlimited # To enable MCQ4structures to run well
RUN echo "" > lib/__init__.py
# Install Java 17 for MCQ4Structures
RUN wget https://download.java.net/openjdk/jdk17/ri/openjdk-17+35_linux-x64_bin.tar.gz && \
    tar -xvf openjdk-17+35_linux-x64_bin.tar.gz && \
    mv jdk-17 /opt/ && \
    rm openjdk-17+35_linux-x64_bin.tar.gz
RUN make install_mcq
RUN rm -rf /var/lib/apt/lists/*
# Copy the needed files
COPY . .
ENTRYPOINT ["python3", "-m", "src.rnadvisor_cli"]


FROM release as dev
RUN apt-get update && apt-get install -y bc vim
ENTRYPOINT ["/bin/bash"]
