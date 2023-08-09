import uuid
from ftplib import FTP
from time import time
from PIL import Image
import os

import ops

FILE_NAME_INDEX = 2

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')


def image_processing(file_name, image_path):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        tmp = image
        path_list += ops.flip(image, file_name)
        path_list += ops.rotate(image, file_name)
        path_list += ops.filter(image, file_name)
        path_list += ops.gray_scale(image, file_name)
        path_list += ops.resize(image, file_name)

    latency = time() - start
    return latency, path_list


def main(args):
    file_name = args['file_name']

    with open(file_name, "wb") as f:
        ftp.retrbinary('RETR ' + 'image/' + file_name, f.write, 1024)
        f.close()

    latency, path_list = image_processing(file_name, file_name)
    os.remove(file_name)

    for path in path_list:
        with open(path, "rb") as f:
            ftp.storbinary('STOR ' + path, f)
            f.close()
        os.remove(path)
    # ftp.quit()
    return {"latency": latency}


'''
{'file-name':'golden_age.png'}
'''