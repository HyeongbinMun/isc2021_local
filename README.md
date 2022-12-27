# ISC 2021

This repository contains code for the Image Similarity Challenge 2021.
origin git : https://github.com/facebookresearch/isc2021

## Installation
환경 설정은 docker를 통해 구현하였으며 환경 설정을 하기 위해서는 아래와 같은 패키지 설치가 필요하다.

docker 환경 : cuda : 11.6.1 / cudnn : 8.0 / ubuntu : 20.04
* [Docker](https://docs.docker.com/engine/install/ubuntu/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* [Nvidia-docker](https://github.com/NVIDIA/nvidia-docker)

1. 해당 패키지 설치 후 docker.compose.yml 파일에서 볼륨 및 포트 변경

```python
# : 기준으로 앞쪽이 자신의 로컬 directory, 뒤쪽이 생성되는 mount directory
    volumes:
      - "/media/mmlab/hdd:/hdd"  # 원하는 디렉토리로 수정
      
# 앞쪽의 25100 ~ 25103 부분의 변경 
    ports:
      - "25100:22"               # ssh port
      - "25101:6006"             # tensorboard port
      - "25102:8000"             # web port
      - "25103:8888"             # jupyter port
      
```

2. docker container 생성 및 접속

```python
docker-compose up -d                # 생성
docker attach [CONTAINER_NAME]      # 접속
```

환경 변경 후 container 재적용 실행 command(단 이전의 작업이 날아갈 수 있음)
```python
docker-compose up -d --build
```

ssh port 접근 이외에 docker container 다중 접속
```python
docker exec -it [CONTAINER_NAME] bash
```

3. 환경 세팅

 - 패키지 설치
```python
conda create -n isc2021 python=3.8 -y && conda activate isc2021
pip install -e workspace/
conda install -c pytorch faiss-gpu
```

```python
export PYTHONPATH="baselines/asmk:baselines/cnnimageretrieval-pytorch-1.2:baselines/how:$PYTHONPATH"

# cirtorch
wget "https://github.com/filipradenovic/cnnimageretrieval-pytorch/archive/v1.2.zip"
unzip v1.2.zip
rm v1.2.zip
export PYTHONPATH=${PYTHONPATH}:$(realpath cnnimageretrieval-pytorch-1.2)
```

 - Install the asmk package with dependencies (see asmk github for details)
```python
 # asmk
pip3 install pyaml numpy faiss-gpu
cd asmk
python3 setup.py build_ext --inplace
rm -r build
cd ..
export PYTHONPATH=${PYTHONPATH}:$(realpath asmk)
 ```

4. 학습

 - train
```python 
python baselines/how/examples/demo_how.py \
    train \
    examples/params/eccv20/train_how_r18.yml -e train_how_r18
```

5. 평가
 - eval
```python 
python baselines/how/examples/demo_how.py \
    eval \
    baselines/how_r50-_2000.yml \
    --step train_codebook
```
```python 
python baselines/how/examples/demo_how.py \
    eval \
    baselines/how_r50-_2000.yml \
    --datasets-local '[{"name": "final_references", "image_root": "/workspace/images/references/*.jpg", "query_list": null, "database_list": "/workspace/list_files/final_references"}]' \
    --step aggregate_database
```
```python 
python baselines/how/examples/demo_how.py \
    eval \
    baselines/how_r50-_2000.yml \
    --datasets-local '[{"name": "final_references", "image_root": "/workspace/images/references/*.jpg", "query_list": null, "database_list": "/workspace/list_files/final_references"}]' \
    --step build_ivf
```
```python 
python baselines/how/examples/demo_how.py \
    eval \
    baselines/how_r50-_2000.yml \
    --datasets-local '[{"name": "final_references", "image_root": "/workspace/images/final_queries/*.jpg", "query_list": "/workspace/list_files/final_queries", "database_list": null}]' \
    --step query_ivf
```
```python 
python baselines/how_find_matches.py \
    baselines/how_r50-_2000.yml \
    1_references \
    --query_list list_files/final_queries \
    --db_list list_files/subset_1_references \
    --preds_filepath data/predictions_how_final_1.csv
```
```python 
python scripts/compute_metrics.py \
    --gt_filepath list_files/subset_1_ground_truth.csv \
    --preds_filepath data/predictions_how_final_1.csv
```
