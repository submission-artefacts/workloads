declare -a memList=(128 256 512 1024 2048 3008 4096 16384)

for mem in ${memList[@]}; do
    docker stop pythonaiactions${mem}m | xargs docker stop
done;
