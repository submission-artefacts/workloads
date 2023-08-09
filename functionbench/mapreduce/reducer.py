import json
from ftplib import FTP
from time import time
import io

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')

computer_language = ["JavaScript", "Java", "PHP", "Python", "C#", "C++",
                     "Ruby", "CSS", "Objective-C", "Perl",
                     "Scala", "Haskell", "MATLAB", "Clojure", "Groovy"]


def main(args):
    job_bucket = args['job_bucket']

    output = {}

    for lang in computer_language:
        output[lang] = 0

    network = 0
    reduce = 0

    # all_keys = []
    # for obj in ftp.nlst(job_bucket):
    #     all_keys.append(obj)
    # print(all_keys)

    for key in ftp.nlst(job_bucket):
        start = time()

        response = io.BytesIO()
        ftp.retrbinary('RETR ' + key, response.write, 1024)
        contents = response.getvalue().decode('utf-8')
        network += time() - start

        start = time()
        data = json.loads(contents)
        for key in data:
            output[key] += data[key]
        reduce += time() - start

    metadata = {
        'output': str(output),
        'network': str(network),
        'reduce': str(reduce)
    }

    return metadata
