import os
from time import time
import cv2
from ftplib import FTP


tmp = "/tmp/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')


def video_processing(file_name, video_path):
    result_file_path = file_name+f'-out.avi'

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            tmp_file_path = tmp+'tmp.jpg'
            cv2.imwrite(tmp_file_path, gray_frame)
            gray_frame = cv2.imread(tmp_file_path)
            out.write(gray_frame)
        else:
            break

    latency = time() - start
    video.release()
    out.release()

    return latency, result_file_path


def main(args):

    file_name = args.get('file_name')

    with open(file_name, "wb") as f:
        ftp.retrbinary('RETR ' + 'video/' + file_name, f.write, 1024)
        f.close()

    latency, path = video_processing(file_name, file_name)

    with open(path, "rb") as f:
        ftp.storbinary('STOR ' + path, f)
        f.close()

    # ftp.quit()
    os.remove(file_name)
    os.remove(path)

    return {"latency": latency}

'''
{"file-name":"office.mp4""}
'''
