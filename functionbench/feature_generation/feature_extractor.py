import io
from ftplib import FTP

import pandas as pd
from time import time
import re

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')

cleanup_re = re.compile('[^a-z]+')


def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


def main(args):
    # bucket = args['input_bucket']
    key = args['key']
    output_bucket = args['output_bucket']
    file_name = key.split('/')[-1]

    with open(file_name, "wb") as f:
        ftp.retrbinary('RETR ' + key, f.write, 1024)
        f.close()

    df = pd.read_csv(file_name)

    start = time()
    df['Text'] = df['Text'].apply(cleanup)
    text = df['Text'].tolist()
    result = set()
    for item in text:
        result.update(item.split())
    print("Number of Feature : " + str(len(result)))

    feature = str(list(result))
    feature = feature.lstrip('[').rstrip(']').replace(' ', '')
    latency = time() - start
    print(latency)

    write_key = output_bucket+'/'+key.split('/')[-1].split('.')[0] + ".ext"
    ftp.storbinary('STOR ' + write_key, io.BytesIO(feature.encode('utf-8')))

    # ftp.quit()
    return {"latency" : latency}


# {"input_bucket": "food_reviews", "key": "food_reviews/reviews10mb.csv"}