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

# Build stage for the voronota : a C++ based code
FROM gcc:9.5.0 AS voronota
WORKDIR /src/
RUN apt-get update
# Install using apt
RUN apt install voronota

# Build stage for the Zhanglab group : a C++ based code
FROM gcc:9.5.0 AS zhanglab
WORKDIR /src/
COPY Makefile .
# Download the TMScore.cpp file and build the binary file
RUN make install_zhanggroup && \
    make build_tm


FROM gcc:9.5.0 as rasp
WORKDIR /src/
COPY Makefile .
# Clone the RASP repo and build the code
RUN make install_rasp
RUN cd lib/rasp ; make rna

FROM python:3.8 as barnaba
# Image not used as this is just a python code
WORKDIR /src
COPY Makefile .
RUN make install_barnaba

FROM gcc:9.5.0 as dfire
WORKDIR src
COPY Makefile .
RUN make install_dfire
RUN cd lib/dfire ; make

FROM gcc:9.5.0 as rs_rnasp
WORKDIR src
COPY Makefile .
RUN make install_rs_rnasp
RUN cd lib/rs_rnasp ; make build

# Final stage for the scoring process, using the previous build stages
FROM python:3.8 as release
WORKDIR /app/
# Copy python requirements - couldn't build an image as this is interpreted
COPY requirements.txt .
# Copy the python code from RNA_Assessment and MC-Annotate binary file
COPY --from=rna_assessment /src/lib/rna_assessment ./lib/rna_assessment
# Copy the code of mcq4structures - the requirements are in a *.jar file
COPY --from=mcq4structures /src/lib/mcq4structures ./lib/mcq4structures
# Copy the binary files
COPY --from=voronota /usr/bin/voronota-* usr/bin/voronota /bin/
# Copy the binary file
COPY --from=zhanglab /src/lib/zhanggroup/ ./lib/zhanggroup
# Copy RASP code
COPY --from=rasp /src/lib/rasp/bin ./lib/rasp/bin
COPY --from=rasp /src/lib/rasp/lib ./lib/rasp/lib
# Copy code from dfire
COPY --from=dfire /src/lib/dfire ./lib/dfire
# Copy code from rsRNASP
COPY --from=rs_rnasp /src/lib/rs_rnasp/ ./lib/rs_rnasp


ENV RASP=/app/lib/rasp
ENV DFIRE_RNA_HOME=/app/lib/dfire
# Install missing requirements
COPY Makefile .
RUN apt-get update &&\
    apt install maven -y  && \
    apt-get install -y --no-install-recommends default-jre-headless
RUN pip install -r requirements.txt
RUN make install_barnaba
RUN echo "" > lib/__init__.py
# Copy the needed files
COPY . .
ENTRYPOINT ["python", "-m", "src.rnadvisor_cli"]

FROM release as dev
RUN apt-get install -y bc vim
ENTRYPOINT ["/bin/bash"]
