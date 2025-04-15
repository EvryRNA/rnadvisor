FROM registry.scicore.unibas.ch/schwede/openstructure
WORKDIR /app

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

RUN find /usr/lib/python3/dist-packages/ -name '*nspkg.pth' -exec rm -v {} +

ENTRYPOINT ["python3", "-m", "rnadvisor.metric.open_structures.lddt_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]