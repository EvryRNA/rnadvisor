# RNAdvisor - Example

## Docker data

In order to not include data inside the docker image, we recommend the use of docker volume. 

To do so, we created a folder `docker_data` that will be the buffer between local files and running container. 

There are two main folders: 

- `docker_data/input`: the input data that will be used
- `docker_data/output`: the output directory where will be saved the different outputs.

## Script 

The `script.sh` pull the docker hub image and then execute it with the `config.yaml` file. 

The `config.yaml` is an example of configuration file that stores the different parameters and file paths for the prediction. 

It runs the following command: 

```bash
docker run -it -v ${PWD}/docker_data/:/app/docker_data -v ${PWD}/config.yaml:/app/config.yaml sayby77/rnadvisor --config_path=./config.yaml
```

The `-v ${PWD}/docker_data/:/app/docker_data` sets a volume that is mapped to the local `docker_data` folder. 

The `-v ${PWD}/config.yaml:/app/config.yaml` sets a volume that is mapped to the local `config.yaml` file.

The `--config_path=./config.yaml` is an argument that is passed to the CLI code.

## Run the script

To run the script with the example, use the following command: 

```bash
./script.sh
```

It should return a file `docker_data/output/rp03.csv` with the different predictions. 

A `docker_data/logs` folder is also created with the different logs.