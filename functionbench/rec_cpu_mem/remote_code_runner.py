import requests
import json
from pprint import pprint
import time
import warnings

warnings.filterwarnings("ignore")
wsk_host = 'wsk-host'
payloads = json.load(open('payloads.json', "r"))
invocations = json.load(open('invocations.json', "r"))


def save_response(action, response):
    with open(f"response/{action}.json", "w+") as js_file:
        json.dump(response, js_file, indent=4)
        js_file.close()


def invoke(action):
    url = f"http://{wsk_host}/api/v1/namespaces/guest/actions/{action}?blocking=true"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic MjNiYzQ2YjEtNzFmNi00ZWQ1LThjNTQtODE2YWE0ZjhjNTAyOjEyM3pPM3haQ0xyTU42djJCS0sxZFhZRnBYbFBrY2NPRnFtMTJDZEFzTWdSVTRWck5aOWx5R1ZDR3VNREdJd1A='
    }
    # payload = json.dumps(payloads[action])
    payload_list = payloads[action]
    for payload in payload_list:
        payload = json.dumps(payload)
        time.sleep(1)
        print(payload)
        response = requests.post(url, headers=headers, data=payload, verify=False).json()
        save_response(action, response)
        print(response['response']) if 'response' in response else print(response)


def invoke_all():
    while True:
        total_num_invotations = 0
        for action in payloads.keys():
            num_invoke = invocations[action]
            print(f"{action}: {num_invoke}")
            if num_invoke > 0:
                try:
                    invoke(action)
                    # pprint(response)
                except Exception as ex:
                    print(f"Error: {ex}")
                    pass
                total_num_invotations += 1
            invocations[action] = num_invoke - 1
            print()
        if total_num_invotations == 0:
            break


def invoke_n_times(action_list, n_times):
    for action, n in zip(action_list, n_times):
        for _ in range(n):
            print(action)
            invoke(action)

# print(invoke_n_times(['matmul', 'linpack', 'float_operation'], [5,5,5]))

# print(invoke('model_training'))
print(invoke_all())
print(requests.get("http://localhost:5000/save"))
