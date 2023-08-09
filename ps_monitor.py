import json
import chompjs
import os
import sys
from time import sleep, time
from uuid import uuid4
import psutil
import resource
import tracemalloc
import subprocess
from fn_caller import call
import signal
from pyloads_js import js_payloads


def signal_handler(signum, frame):
    print("Received SIGALRM [%s]" % signum)
    raise Exception("Timed out!")


signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(300)  # introduce a 300 seconds TL on functions


def monitor_python_call(fn_name, rep):
    process = psutil.Process()

    pid = process.pid

    net_cmd = f"cat /proc/{pid}/net/dev | grep eth0 | " + "awk '{print $2,$3,$10,$11}'"
    before_bytes_rx, before_pkgs_rx, before_bytes_tx, before_pkgs_tx = subprocess.getoutput(cmd=net_cmd).split(" ")
    start_cpu_usage = process.cpu_times()
    before_resource_usage = resource.getrusage(resource.RUSAGE_SELF)
    start_memory_usage = process.memory_info()
    start_num_ctx_switches = process.num_ctx_switches()
    start_io_counters = process.io_counters()
    tracemalloc.start()
    duration_start = time()

    try:
        call(fn_name, rep)
    except Exception as ex:
        print(f"{fn_name} {rep}: {ex}")

    duration = time() - duration_start
    end_cpu_usage = process.cpu_times()
    after_resource_usage = resource.getrusage(resource.RUSAGE_SELF)
    end_memory_usage = process.memory_info()
    end_num_ctx_switches = process.num_ctx_switches()
    end_io_counters = process.io_counters()

    allocated_memory, peak_memory = tracemalloc.get_traced_memory()
    snapshot = tracemalloc.take_snapshot()
    stats = snapshot.statistics('traceback')
    total_heap_size = sum(stat.size for stat in stats)
    used_heap_size = sum(stat.size for stat in stats if stat.count > 0)

    after_bytes_rx, after_pkgs_rx, after_bytes_tx, after_pkgs_tx = subprocess.getoutput(cmd=net_cmd).split(" ")

    return {
        "id": str(uuid4()),
        "duration": int(duration * 1e3),  # millisecs
        "maxRss": after_resource_usage.ru_maxrss - before_resource_usage.ru_maxrss,
        "fsRead": end_io_counters.read_count - start_io_counters.read_count,
        "fsWrite": end_io_counters.write_count - start_io_counters.write_count,
        "vContextSwitches": end_num_ctx_switches.voluntary - start_num_ctx_switches.voluntary,
        "ivContextSwitches": end_num_ctx_switches.involuntary - start_num_ctx_switches.involuntary,
        "userDiff": (end_cpu_usage.user - start_cpu_usage.user) * 1e6,  # microsecs
        "sysDiff": (end_cpu_usage.system - start_cpu_usage.system) * 1e6,
        "rss": (end_memory_usage.rss - start_memory_usage.rss) / 1024,
        "heapTotal": total_heap_size,  # ??
        "heapUsed": used_heap_size,  # ??
        "mallocMem": allocated_memory,
        "netByRx": int(after_bytes_rx) - int(before_bytes_rx),
        "netPkgRx": int(after_pkgs_rx) - int(before_pkgs_rx),
        "netByTx": int(after_bytes_tx) - int(before_bytes_tx),
        "netPkgTx": int(after_pkgs_tx) - int(before_pkgs_tx)
    }


def monitor_js_call(fn_name, mem, rep=0, fn_type='synthetic'):
    if fn_type == 'synthetic':
        run_cmd = f"cd syntheticfunctiongenerator/function_generator/build/{fn_name}-{mem}/ && node -e 'require(\"./function\").handler()'"
    else:
        payload = json.dumps(js_payloads[fn_name][rep])
        run_cmd = f"cd serverlessbench/data_analysis/src/ && node -e 'require(\"./{fn_name}-monitor\").handler({payload})'"
    output = subprocess.getoutput(cmd=run_cmd).split(" ")
    output = ''.join(output).replace('\n', '')
    return chompjs.parse_js_object(output)


split = sys.argv[1]
fn_name = sys.argv[2]
rep = int(sys.argv[3]) - 1
mem_size = sys.argv[4]

if split == "train":
    data = monitor_js_call(fn_name=fn_name, mem=mem_size)
    if not os.path.exists(f"training-data/{fn_name}-{mem_size}.jsonl"):
        os.system(f"mkdir -p training-data/")

    with open(f"training-data/{fn_name}-{mem_size}.jsonl", "a+") as out_file:
        out_file.write(json.dumps(data) + '\n')

else:
    js_fns = ["wage-insert", "wage-format", "wage-db-writer"]
    if fn_name in js_fns:
        data = monitor_js_call(fn_name=fn_name, mem=mem_size, rep=rep, fn_type='valid')
    else:
        data = monitor_python_call(fn_name=fn_name, rep=rep)
    if not os.path.exists(f"validation-data/{mem_size}MB/Repetition_{rep}/{fn_name}.jsonl"):
        os.system(f"mkdir -p validation-data/{mem_size}MB/Repetition_{rep}/")

    with open(f"validation-data/{mem_size}MB/Repetition_{rep}/{fn_name}.jsonl", "a+") as out_file:
        out_file.write(json.dumps(data) + '\n')

# print(json.dumps(data, indent=4))
