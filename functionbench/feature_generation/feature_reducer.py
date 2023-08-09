import io
from ftplib import FTP

from time import time
from sklearn.feature_extraction.text import TfidfVectorizer

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')


def main(args):
    bucket = args['input_bucket']

    result = []
    latency = 0

    for obj in ftp.nlst(bucket):
        if obj.split('.')[-1] != 'ext':
            continue
        bytes_io = io.BytesIO()
        ftp.retrbinary('RETR ' + obj, bytes_io.write)
        body = bytes_io.getvalue().decode('utf-8')
        start = time()
        word = body.replace("'", '').split(',')
        result.extend(word)
        latency += time() - start

    print(len(result))

    tfidf_vect = TfidfVectorizer().fit(result)
    feature = str(tfidf_vect.get_feature_names())
    feature = feature.lstrip('[').rstrip(']').replace(' ', '')

    feature_key = 'feature.txt'
    ftp.storbinary('STOR ' + feature_key, io.BytesIO(feature.encode('utf-8')))

    return {"latency": latency}

# if __name__ == '__main__':
#     main({"input_bucket": "extracted"})

