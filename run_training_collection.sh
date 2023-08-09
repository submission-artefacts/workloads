#!/bin/bash

declare -a memList=(128 256 512 1024 2048 3008 4096 16384)
declare -a repList=(1 2 3)
cd syntheticfunctiongenerator/function_generator
go build
./synthetic-function-generator generate --dependency-layern-arn LAYER_ARN --func-segments ../function_segments \
--lambda-role-arn LAMBDA_ROLE_ARN --replay ../replay_train.txt -s 128,256,512,1024,2048,3008
cd ../..
for mem in ${memList[@]}; do
      echo ============================== ${mem}MB ==============================;
      docker run -d --env PATH=$PATH:/.node/bin --name pythonaiactions${mem}m shariar076/python3aiaction
      docker cp ~/node.tar.gz pythonaiactions${mem}m:/
      docker exec pythonaiactions${mem}m bash -c "tar -xzf node.tar.gz && chown -R root:root .node"
      docker exec pythonaiactions${mem}m bash -c "npm i lorem-ipsum uuid sharp mathjs ftp json-to-pretty-yaml js-image-generator"
      docker exec  pythonaiactions${mem}m pip install chompjs psutil
      docker cp ./ pythonaiactions${mem}m:/workloads

      docker update --cpus 1  --memory ${mem}m pythonaiactions${mem}m
      docker exec -d pythonaiactions${mem}m bash -c "cd workloads ; ./collect_training_metrices.sh ${mem} 1 > collection.log;"
    done;
