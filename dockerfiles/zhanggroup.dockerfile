FROM python:3.10 as zhanggroup

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mkdir -p lib/zhanggroup


FROM zhanggroup as tm_score


#RUN wget -O lib/zhanggroup/TMscore.cpp https://zhanggroup.org/TM-score/TMscore.cpp && \
#    g++ -static -O3 -ffast-math -lm lib/zhanggroup/TMscore.cpp -o lib/zhanggroup/TMscore

RUN wget -O lib/zhanggroup/USalign.cpp https://zhanggroup.org/US-align/bin/module/USalign.cpp && \
    g++ -O3 -lm -o lib/zhanggroup/USalign lib/zhanggroup/USalign.cpp

#RUN chmod +x lib/zhanggroup/TMscore
RUN chmod +x lib/zhanggroup/USalign

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

ENTRYPOINT ["python", "-m", "rnadvisor.metric.zhanggroup.tm_score_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]

FROM zhanggroup as gdt_ts


RUN wget -O lib/zhanggroup/TMscore.cpp https://zhanggroup.org/TM-score/TMscore.cpp && \
    g++ -static -O3 -ffast-math -lm lib/zhanggroup/TMscore.cpp -o lib/zhanggroup/TMscore

RUN chmod +x lib/zhanggroup/TMscore

COPY requirements/wrapper-requirements.txt wrapper.txt
RUN pip install --no-cache-dir -r wrapper.txt

COPY src/rnadvisor /app/rnadvisor
COPY data/example /app/data/example

ENTRYPOINT ["python", "-m", "rnadvisor.metric.zhanggroup.gdt_ts_helper"]
CMD ["--pred_dir=data/example/PREDS", "--native_path=data/example/NATIVE/R1107.pdb"]
