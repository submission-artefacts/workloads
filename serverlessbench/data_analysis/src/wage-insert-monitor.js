/*
 * Copyright (c) 2020 Institution of Parallel and Distributed System, Shanghai Jiao Tong University
 * ServerlessBench is licensed under the Mulan PSL v1.
 * You can use this software according to the terms and conditions of the Mulan PSL v1.
 * You may obtain a copy of Mulan PSL v1 at:
 *     http://license.coscl.org.cn/MulanPSL
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
 * PURPOSE.
 * See the Mulan PSL v1 for more details.
 */

const Validator = require('node-input-validator').Validator;
const ROLES = require('./constances').ROLES;

function callFormatter(requestJSON) {
    var request = require('request');
    var options = {
        'method': 'POST',
        'url': 'http://wsk-host/api/v1/namespaces/guest/actions/wage-format?blocking=true&result=true',
        'headers': {
        'Content-Type': 'application/json',
        'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A='
    },
    body: JSON.stringify(requestJSON)
    };
    request(options, function (error, response) {
        if (error){
            console.error('failed to invoke action:', error);
        }
//        console.log('invoke wage-db-writer result:', JSON.stringify(response.body));
    });
}

async function check (params) {
    // check format
    const v = new Validator(params, {
        id: 'required|numeric',
        name: 'required|string',
        role: 'required|string',
        base: 'required|decimal|digitsBetween:1,8',
        merit: 'required|decimal|digitsBetween:1,8',
        operator: 'required|numeric'
    });

    const matched = await v.check();

    if(!matched) {
        return {'result': 'fail: illegal params:'+JSON.stringify(params)};
    }
    
    // check role
    if (!ROLES.includes(params.role)) {
        return {'result': 'fail: invalid role:'+params.role};
    }
    
    return true;
}

function main (params) {
//    console.log('[wage-insert] entry');

    check(params).then( passOrErr => {
        if (typeof passOrErr !== 'boolean') {
            console.log('check result:', passOrErr, ',type:', typeof passOrErr);
            return passOrErr;
        }

//        console.log('Checks passed, calling formatter');

        return callFormatter(params);
    }).catch(err => {
        console.log('wage-check err:', err);
    });
}

async function handler(params, payload) {
  const child_process = require("child_process");
  const v8 = require("v8");
  const {performance, PerformanceObserver, monitorEventLoopDelay } = require("perf_hooks");
  const [beforeBytesRx, beforePkgsRx, beforeBytesTx, beforePkgsTx] =
    child_process.execSync("cat /proc/net/dev | grep eth0 | awk '{print $2,$3,$10,$11}'").toString().split(" ");
  const startUsage = process.cpuUsage();
  const beforeResourceUsage = process.resourceUsage();
  const wrapped = performance.timerify(payload);
  const h = monitorEventLoopDelay();
  h.enable();


  const durationStart = process.hrtime();

  await wrapped(params);
  h.disable();

  const durationDiff = process.hrtime(durationStart);
  const duration = (durationDiff[0] * 1e9 + durationDiff[1]) / 1e6

  // Process CPU Diff
  const cpuUsageDiff = process.cpuUsage(startUsage);
  // Process Resources
  const afterResourceUsage = process.resourceUsage();

  // Memory
  const heapCodeStats = v8.getHeapCodeStatistics();
  const heapStats = v8.getHeapStatistics();
  const heapInfo = process.memoryUsage();

  // Network
  const [afterBytesRx, afterPkgsRx, afterBytesTx, afterPkgsTx] =
    child_process.execSync("cat /proc/net/dev | grep eth0 | awk '{print $2,$3,$10,$11}'").toString().split(" ");

  const { v4: uuidv4 } = require('uuid');
  console.log({
      "id": uuidv4(),
      "duration": `${duration}`,
      "maxRss": `${afterResourceUsage.maxRSS - beforeResourceUsage.maxRSS}`,
      "fsRead": `${afterResourceUsage.fsRead - beforeResourceUsage.fsRead}`,
      "fsWrite": `${afterResourceUsage.fsWrite - beforeResourceUsage.fsWrite}`,
      "vContextSwitches": `${afterResourceUsage.voluntaryContextSwitches - beforeResourceUsage.voluntaryContextSwitches}`,
      "ivContextSwitches": `${afterResourceUsage.involuntaryContextSwitches - beforeResourceUsage.involuntaryContextSwitches}`,
      "userDiff": `${cpuUsageDiff.user}`,
      "sysDiff": `${cpuUsageDiff.system}`,
      "rss": `${heapInfo.rss}`,
      "heapTotal": `${heapInfo.heapTotal}`,
      "heapUsed": `${heapInfo.heapUsed}`,
      "external": `${heapInfo.external}`,
      "elMin": `${h.min}`,
      "elMax": `${h.max}`,
      "elMean": `${isNaN(h.mean)? 0 : h.mean}`,
      "elStd": `${isNaN(h.stddev)? 0 : h.stddev}`,
      "bytecodeMetadataSize": `${heapCodeStats.bytecode_and_metadata_size}`,
      "heapPhysical": `${heapStats.total_physical_size}`,
      "heapAvailable": `${heapStats.total_available_size}`,
      "heapLimit": `${heapStats.heap_size_limit}`,
      "mallocMem": `${heapStats.malloced_memory}`,
      "netByRx": `${afterBytesRx - beforeBytesRx}`,
      "netPkgRx": `${afterPkgsRx - beforePkgsRx}`,
      "netByTx": `${afterBytesTx - beforeBytesTx}`,
      "netPkgTx": `${afterPkgsTx - beforePkgsTx}`
    })

  return {
    'statusCode': 200
  };
};

//exports.main = main

exports.handler = async (params) => {
  return await handler(params, main);
}

