#!/bin/bash

# Load the docker image
docker pull sayby77/rnadvisor:latest
# Launch the container
docker run -it -v ${PWD}/docker_data/:/app/docker_data -v ${PWD}/config.yaml:/app/config.yaml sayby77/rnadvisor --config_path=./config.yaml