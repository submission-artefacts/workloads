#!/bin/bash


declare -a funcList=("compress-floatoperations-ftpread" "compress-ftpread-ftpread" "compress-imageresize-writefile"
                      "compress-imagerotate-imagecompress" "compress-ftpread" "compress-compress-readfile"
                      "compress-imageresize-imageresize-json2yaml" "compress-compress-matmul" "compress-ftpread-imagecompress"
                      "compress-ftpwrite-decompress" "compress-floatoperations-json2yaml" "compress-decompress-ftpwrite-json2yaml"
                      "compress-imagecompress-imagerotate" "compress-ftpwrite-json2yaml" "compress-compress-imageresize"
                      "compress-floatoperations-ftpwrite" "compress-decompress-readfile" "compress-compress"
                      "compress-imagecompress-ftpwrite" "compress-imageresize-sleep-compress" "compress-imagecompress-compress"
                      "compress-ftpwrite-writefile" "compress-ftpread-compress" "compress-imagerotate-compress"
                      "compress-imageresize-ftpwrite" "compress-ftpread-json2yaml" "compress-imagecompress-writefile"
                      "compress-ftpread-floatoperations" "compress-imagerotate-floatoperations-decompress" "compress-compress-json2yaml" )

mem=$1
rep=$2

# Read the array values with space
for fn in "${funcList[@]}"; do
 echo ============================== $fn ==============================;
 # openwhisk default 300s time limit
 for f in {0..100}; do python ps_monitor.py train $fn $rep $mem; sleep .1; done;
done