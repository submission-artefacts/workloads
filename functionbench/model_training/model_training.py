import os
from ftplib import FTP

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

import pandas as pd
from time import time
import re
import io

cleanup_re = re.compile('[^a-z]+')
tmp = '/tmp/'

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')


def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence


def main(args):
    dataset_bucket = args['dataset_bucket']
    dataset_name = args['dataset_name']
    model_bucket = args['model_bucket']
    model_name = args['model_name']  # example : lr_model.pk

    # ftp_host = os.popen('curl ipinfo.io/ip').read()

    with open(dataset_name, "wb") as f:
        ftp.retrbinary('RETR ' + f"{dataset_bucket}/{dataset_name}", f.write, 1024)
        f.close()

    df = pd.read_csv(dataset_name)

    start = time()
    df['train'] = df['Text'].apply(cleanup)

    tfidf_vector = TfidfVectorizer(min_df=100).fit(df['train'])

    train = tfidf_vector.transform(df['train'])

    model = LogisticRegression()
    model.fit(train, df['Score'])
    latency = time() - start

    joblib.dump(model, model_name)

    with open(model_name, "rb") as f:
        ftp.storbinary('STOR ' + f"{model_bucket}/{model_name}", f)
        f.close()

    # ftp.quit()
    os.remove(dataset_name)
    os.remove(model_name)
    return {"latency": latency}


'''
sample_payload
{'dataset-name':'reviews20mb.csv', 'model-name':'sample.joblib'}
'''
