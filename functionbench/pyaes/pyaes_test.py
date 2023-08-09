import os
from ftplib import FTP
from time import time
import random
import string
import pyaes

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')


def generate(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def main(args):
    length_of_message = int(args['length_of_message'])
    num_of_iterations = int(args['num_of_iterations'])

    out_file_path = "pyaes-out.txt"

    message = generate(length_of_message)

    # 128-bit key (16 bytes)
    KEY = b'\xa1\xf6%\x8c\x87}_\xcd\x89dHE8\xbf\xc9,'

    with open(out_file_path, "w+") as out_file:
        start = time()
        for loops in range(num_of_iterations):
            out_file.write(f"#loop:{loops}\n")
            aes = pyaes.AESModeOfOperationCTR(KEY)
            ciphertext = aes.encrypt(message)
            out_file.write(ciphertext.hex()+'\n')

            aes = pyaes.AESModeOfOperationCTR(KEY)
            plaintext = aes.decrypt(ciphertext)
            out_file.write(plaintext.hex()+'\n')
            aes = None
        out_file.close()

    with open(out_file_path, "rb") as f:
        ftp.storbinary('STOR ' + out_file_path, f)
        f.close()

    # ftp.quit()
    os.remove(out_file_path)
    latency = time() - start
    return {"latency": latency}


'''
{'length-of-message':'50','num-of-iterations':'100'}
'''