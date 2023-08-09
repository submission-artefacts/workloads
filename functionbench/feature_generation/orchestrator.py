from time import time
import json
from ftplib import FTP
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

import requests

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')

wsk_host = "wsk-host"


def invoke(action, payload):
    url = f"http://{wsk_host}/api/v1/namespaces/guest/actions/{action}?blocking=true"

    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A='
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    return response.json()['response']


def invoke_lambda(output_bucket, key):
    invoke(
        action='feature_extractor',
        payload=json.dumps({
            "key": key,
            "output_bucket": output_bucket
        })
    )


def main(args):
    input_bucket = args['input_bucket']
    output_bucket = args['output_bucket']
    start = time()
    all_keys = []

    for obj in ftp.nlst(input_bucket):
        all_keys.append(obj)

    pool = ThreadPool(len(all_keys))
    pool.map(partial(invoke_lambda, output_bucket), all_keys)
    pool.close()
    pool.join()
    latency = time() - start
    return {"num_of_file": len(all_keys), "latency": latency}

