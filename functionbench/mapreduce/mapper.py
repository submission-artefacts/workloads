import json
from time import time
from ftplib import FTP
import io

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')

subs = "</title><text>"
computer_language = ["JavaScript", "Java", "PHP", "Python", "C#", "C++",
                     "Ruby", "CSS", "Objective-C", "Perl",
                     "Scala", "Haskell", "MATLAB", "Clojure", "Groovy"]


def main(args):
    job_bucket = args['job_bucket']
    src_bucket = args['bucket']
    src_keys = args['keys']
    mapper_id = args['mapper_id']

    output = {}

    for lang in computer_language:
        output[lang] = 0

    network = 0
    map = 0
    keys = src_keys.split('/')

    # Download and process all keys
    for key in keys:
        start = time()
        # response = s3_client.get_object(Bucket=src_bucket, Key=key)
        response = io.BytesIO()
        ftp.retrbinary('RETR ' + f"{src_bucket}/{key}", response.write, 1024)
        contents = response.getvalue().decode('utf-8')

        network += time() - start

        start = time()
        for line in contents.split('\n')[:-1]:
            idx = line.find(subs)
            text = line[idx + len(subs): len(line) - 16]
            for lang in computer_language:
                if lang in text:
                    output[lang] += 1

        map += time() - start

    # print(output)

    metadata = {
        'output': str(output),
        'network': str(network),
        'map': str(map)
    }

    start = time()

    ftp.storbinary('STOR ' + f"{job_bucket}/{mapper_id}", io.BytesIO(json.dumps(output).encode('utf-8')))
    network += time() - start
    
    return metadata
