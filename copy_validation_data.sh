declare -a memList=(128 256 512 1024 2048 3008 4096 16384)
declare -a repList=(1 2 3)

for mem in ${memList[@]}; do
    for rep in ${repList[@]}; do
    docker cp pythonaiactions${mem}m${rep}:/workloads/validation-data .
    done;
done;
