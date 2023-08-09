# Description
directory contains the workloads from [FunctionBench](https://github.com/ddps-lab/serverless-faas-workbench) and [ServerlessBench](https://github.com/SJTU-IPADS/ServerlessBench) which are used for benchmarking the system. These modified to work with openwhisk according to the necessary use-cases

# Action/Function Creation
## FunctionBench actions:
These functions require a FTP server for the input and output. Setup an FTP server and upload the contents from `dataset.tar.gz` to a directory called `files` in it. You'll also need to change the host and credentials accordingly in the functions.

1. The functions can be created using:
    ```shell
    cd workloads/functionbench
    ./action_creation.sh
    ```

2. To invoke the functions go to the `functionbench/rec_cpu_mem` directory and update the num of invocations in the `invocations.json` or keep the default. You can change the payloads of the functions in `payloads.json`

3. Finally run the python script `remote_code_runner.py`

## ServerlessBench actions:
1. These functions can be created using:
    ```shell
    cd workloads/serverlessbench
    ./action_creation.sh
    ```
2. To invoke the functions run:
    ```shell
    ./action_invocation.sh
    ```
## Synthetic actions:

```shell
cd syntheticfunctiongenerator/function_generator/
go build .
./synthetic-function-generator generate --dependency-layern-arn LAYER_ARN --func-segments ../function_segments --lambda-role-arn LAMBDA_ROLE_ARN --replay ../replay_train.txt -s 128,256,512,1024,2048,3008
cd <fn-directory>
node -e 'require("./function").handler()'

npm i -g lorem-ipsum uuid sharp mathjs ftp json-to-pretty-yaml js-image-generator
npm i axios@0.21
```