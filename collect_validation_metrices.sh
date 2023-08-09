#!/bin/bash


declare -a funcList=("linpack" "matmul" "chameleon" "video_processing" "image_processing" 
                    "model_training" "pyaes" "feature_extractor" "feature_reducer" "mapper"  "reducer"
                    "cnn_image_classification"  "ml_lr_prediction" "ml_video_face_detection" 
                    "rnn_generate_character_level" "float_operation" "driver" "orchestrator"
                    "alloc_res" "wage-insert" "wage-format" "wage-db-writer")

mem=$1
rep=$2

# Read the array values with space
for fn in "${funcList[@]}"; do
 echo ============================== $fn ==============================;
# openwhisk default 300s time limit
 for f in {0..100}; do python ps_monitor.py validation $fn $rep $mem; sleep .1; done;
done
