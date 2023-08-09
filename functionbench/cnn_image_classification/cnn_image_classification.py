from ftplib import FTP
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import uuid
from time import time
import os

from squeezenet import SqueezeNet

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')

tmp = "./"


def predict(img_local_path):
    start = time()
    model = SqueezeNet(weights='imagenet')
    img = image.load_img(img_local_path, target_size=(227, 227))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    res = decode_predictions(preds)
    latency = time() - start
    return latency, res


def main(args):
    input_bucket = args['input_bucket']
    object_key = args['object_key']
    model_object_key = args['model_object_key']  # example : squeezenet_weights_tf_dim_ordering_tf_kernels.h5
    model_bucket = args['model_bucket']

    download_path = tmp + '{}'.format(object_key)
    # s3_client.download_file(input_bucket, object_key, download_path)
    with open(download_path, "wb") as f:
        ftp.retrbinary('RETR ' + f"{input_bucket}/{object_key}", f.write, 1024)
        f.close()

    model_path = tmp + '{}'.format(model_object_key)
    # s3_client.download_file(model_bucket, model_object_key, model_path)
    with open(model_path, "wb") as f:
        ftp.retrbinary('RETR ' + f"{model_bucket}/{model_object_key}", f.write, 1024)
        f.close()

    latency, result = predict(download_path)
        
    _tmp_dic = {x[1]: {'N': str(x[2])} for x in result[0]}
    os.remove(download_path)
    os.remove(model_path)
    return {"latency": latency, "result": str(result)}
