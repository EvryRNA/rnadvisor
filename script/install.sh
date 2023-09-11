#!/bin/bash

function install_rna_assessment(){
  git clone https://github.com/clementbernardd/RNA_assessment.git --branch scoring-version ../lib/rna_assessment
}

function install_mcq4structures(){
  git clone https://github.com/tzok/mcq4structures.git ../lib/mcq4structures
  mvn -B package --file ../lib/mcq4structures/pom.xml
}

function install_voronota(){
  apt-get install voronota
}

function install_zhanglab(){
	mkdir -p ../lib/zhanggroup
	wget -O ../lib/zhanggroup/TMscore.cpp https://zhanggroup.org/TM-score/TMscore.cpp
}

function install_packages(){
  apt install maven -y
  apt-get install -y --no-install-recommends default-jre-headless
  pip install -r ../requirements.txt
}


function install_local(){
  # Install maven and java
  install_packages;
  # Install the different repos
  install_rna_assessment;
  install_mcq4structures;
  install_voronota;
  install_zhanglab;
}

install_local;