from ftplib import FTP

ftp = FTP("localhost")
ftp.login(user='ftpuser', passwd='ftpuser')
ftp.cwd('files')


def main(args):
    num_of_file = int(args['num_of_file'])
    bucket = args['input_bucket']
    # all_keys = []

    # for obj in ftp.nlst(bucket):
    #     all_keys.append(obj)
    print("Number of File : " + str(len(ftp.nlst(bucket))))
    
    if num_of_file == len(ftp.nlst(bucket)):
        return {"status": "SUCCEEDED"}
    else:
        return {"status": "FAILED"}

