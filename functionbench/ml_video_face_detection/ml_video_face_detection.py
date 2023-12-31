import os
from ftplib import FTP
from time import time
import cv2

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')

tmp = "./"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2


def video_processing(object_key, video_path, model_path):
    file_name = object_key.split(".")[FILE_NAME_INDEX]
    result_file_path = tmp+file_name+'-detection.avi'

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    face_cascade = cv2.CascadeClassifier(model_path)

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            # print("Found {0} faces!".format(len(faces)))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            out.write(frame)
        else:
            break

    latency = time() - start

    video.release()
    out.release()

    return latency, result_file_path


def main(args):
    input_bucket = args['input_bucket']
    object_key = args['object_key']
    output_bucket = args['output_bucket']

    model_object_key = args['model_object_key'] # example : haarcascade_frontalface_default.xml
    model_bucket = args['model_bucket']

    download_path = tmp+'{}'.format(object_key)
    # s3_client.download_file(input_bucket, object_key, download_path)
    with open(download_path, "wb") as f:
        ftp.retrbinary('RETR ' + f"{input_bucket}/{object_key}", f.write, 1024)
        f.close()

    model_path = tmp + '{}'.format(model_object_key)
    # s3_client.download_file(model_bucket, model_object_key, model_path)
    with open(model_path, "wb") as f:
        ftp.retrbinary('RETR ' + f"{model_bucket}/{model_object_key}", f.write, 1024)
        f.close()

    latency, upload_path = video_processing(object_key, download_path, model_path)

    # s3_client.upload_file(upload_path, output_bucket, upload_path.split("/")[FILE_PATH_INDEX])
    with open(upload_path, "rb") as f:
        ftp.storbinary('STOR ' + f"{output_bucket}/{upload_path.split('/')[-1]}", f)
        f.close()
    os.remove(download_path)
    os.remove(model_path)
    os.remove(upload_path)
    return {"latency": latency}
