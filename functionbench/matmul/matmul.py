import numpy as np
from time import time,sleep

def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    # C = np.matmul(A, B)
    sleep(10)
    latency = time() - start
    return latency


def main(args):
    n = int(args.get('n'))
    latency = matmul(n)
    print(latency)
    return {"latency": latency}
