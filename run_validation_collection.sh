#!/bin/bash

declare -a memList=(128 256 512 1024 2048 3008 4096 16384)
declare -a repList=(1 2 3)

export TESTCASE4_HOME=$(pwd)/serverlessbench
pushd ./serverlessbench && grep -rl "wsk-host" | xargs sed -i "s|wsk-host|$(curl ipinfo.io/ip)|g"
./data_analysis/scripts/deploy.sh && popd

for mem in ${memList[@]}; do
    for rep in ${repList[@]}; do
        echo ============================== ${mem}MB  ${rep} ==============================;
        docker run -d --env PATH=$PATH:/.node/bin --env TESTCASE4_HOME=/workloads/serverlessbench --name pythonaiactions${mem}m${rep} shariar076/python3aiaction
        docker cp ~/node.tar.gz pythonaiactions${mem}m${rep}:/
        docker exec pythonaiactions${mem}m${rep} bash -c "tar -xzf node.tar.gz && chown -R root:root .node"
        docker exec pythonaiactions${mem}m${rep} pip install psutil pyaes Chameleon chompjs
        docker cp ./ pythonaiactions${mem}m${rep}:/workloads
        # for composite functions there has to be local openwhisk running
        docker exec pythonaiactions${mem}m${rep} bash -c 'cd /workloads && grep -rl "wsk-host" | xargs sed -i "s|wsk-host|$(curl ipinfo.io/ip)|g"'
        wsk -i action update mapper functionbench/mapreduce/mapper.py --timeout 300000
        wsk -i action update reducer functionbench/mapreduce/reducer.py --timeout 300000
        wsk -i action update feature_extractor functionbench/feature_generation/feature_extractor.py --docker shariar076/python3aiaction --timeout 300000
        docker update --cpus 1  --memory ${mem}m pythonaiactions${mem}m${rep}
        docker exec -d pythonaiactions${mem}m${rep} bash -c "cd workloads ; ./collect_validation_metrices.sh ${mem} ${rep} > collection.log;"
        done;
    done;
