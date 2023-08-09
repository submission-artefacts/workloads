import json
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
import time
from ftplib import FTP
import requests

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')
wsk_host= "wsk-host"

def invoke(action, payload):
    url = f"http://{wsk_host}/api/v1/namespaces/guest/actions/{action}?blocking=true"

    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A='
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)

    return response.json()['response']

total_map = 0
total_network = 0


def map_invoke_lambda(job_bucket, bucket, all_keys, batch_size, mapper_id):
    keys = all_keys[int(mapper_id * batch_size): int((mapper_id + 1) * batch_size)]
    key = ""
    for item in keys:
        key += item + '/'
    key = key[:-1]

    response = invoke(
        action='mapper',
        payload=json.dumps({
            "job_bucket": job_bucket,
            "bucket": bucket,
            "keys": key,
            "mapper_id": mapper_id
        })
    )

    json_data = response['result']

    global total_map, total_network
    total_map += float(json_data['map'])
    total_network += float(json_data['network'])


def reduce_invoke_lambda(job_bucket):
    response = invoke(
        action='reducer',
        payload=json.dumps({
            "job_bucket": job_bucket
        })
    )
    return response['result']


def main(args):
    job_bucket = args['job_bucket']
    src_bucket = args['bucket']
    n_mapper = args['n_mapper']

    ret_response = {}
    # Fetch all the keys
    all_keys = []
    for obj in ftp.nlst(src_bucket):
        all_keys.append(obj.split('/')[-1])

    ret_response["dataset file"] = str(len(all_keys))
    ret_response["key name"] = str(all_keys)

    total_size = len(all_keys)
    batch_size = 0

    if total_size % n_mapper == 0:
        batch_size = total_size / n_mapper
    else:
        batch_size = total_size // n_mapper + 1

    for idx in range(n_mapper):
        ret_response["mapper-" + str(idx)] = str(all_keys[int(idx * batch_size): int((idx + 1) * batch_size)])

    pool = ThreadPool(n_mapper)
    invoke_lambda_partial = partial(map_invoke_lambda, job_bucket, src_bucket, all_keys, batch_size)
    pool.map(invoke_lambda_partial, range(n_mapper))
    pool.close()
    pool.join()

    while True:
        job_keys = ftp.nlst(job_bucket)
        # print("Wait Mapper Jobs ...")
        time.sleep(5)
        if len(job_keys) == n_mapper:
            # print("[*] Map Done : mapper " + str(len(job_keys)) + " finished.")
            break

    ret_response["map"] = str(total_map)
    ret_response["network"] =str(total_network)

    # Reducer
    ret_response["reducer_output"] = reduce_invoke_lambda(job_bucket)

    return ret_response
