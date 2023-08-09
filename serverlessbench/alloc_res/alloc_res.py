# Copyright (c) 2020 Institution of Parallel and Distributed System, Shanghai Jiao Tong University
# ServerlessBench is licensed under the Mulan PSL v1.
# You can use this software according to the terms and conditions of the Mulan PSL v1.
# You may obtain a copy of Mulan PSL v1 at:
#     http://license.coscl.org.cn/MulanPSL
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v1 for more details.

import time
import json
from subprocess import call
import os, stat
import utils

global memCDFFilename, execCDFFilename
memCDFFilename  = "./serverlessbench/alloc_res/CDFs/memCDF.csv"
execCDFFilename = "./serverlessbench/alloc_res/CDFs/execTimeCDF.csv"

def main(args):
    """Main."""
    startTime = utils.getTime()
    sequence = args.get('sequence')
    search_val = args.get('search_val')
    if sequence is None:
        sequence = 0
    else:
        sequence += 1
    
    mmStartTime = utils.getTime()
    memSize = mallocMem(search_val)
    mmEndTime = utils.getTime()

    mmExecTime = mmEndTime - mmStartTime

    execTime = getExecTime(mmExecTime, search_val)
    
    return { 'sequence': sequence,
        'startTime': startTime,
        'memSize': memSize,
        'execTime': execTime
    }

def mallocMem(search_val):
    filename = memCDFFilename
    bias = 30
    mem = utils.getValueRefByCDF(filename, search_val) - bias
    print("Alloc random memory: %d" %(mem))
    os.chmod("./serverlessbench/alloc_res/function",stat.S_IRWXU)
    call(["./serverlessbench/alloc_res/function","%s" %mem])
    return mem

def getExecTime(mmExecTime, search_val):
    filename = execCDFFilename
    execTime = utils.getValueRefByCDF(filename, search_val)
    
    exactAluTime = execTime - mmExecTime
    if exactAluTime > 0:
        utils.alu(exactAluTime)
    print("Execute random time: %d" %(execTime))
    return execTime

# # Use to debug
if __name__ == '__main__':
    memCDFFilename = "CDFs/memCDF.csv"
    execCDFFilename="CDFs/execTimeCDF.csv"
    print(main({"sequence": 0, "search_val": 0.999}))
