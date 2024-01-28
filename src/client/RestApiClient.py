import requests
import json
import os
import platform

from time import sleep
from utils import get_info

url = "http://127.0.0.1:3000"
device_id = 3   # TODO: Need to de initialized during first connection to the server
timeout = 2     # TODO: Can be moved somewhere


def preparing_json():
    resources_obj = get_info()
    json_result = json.dumps(resources_obj.dict(), default=str, indent=4)
    return json.loads(json_result)


while True:
    payload = preparing_json()
    response = requests.post(f"{url}/resources", json=payload)

    if response.status_code != 200:
        print(f"Something went wrong. Error code: {response.status_code}")
        break

    response = requests.get(f"{url}/action/{device_id}?system={platform.system()}")

    if response.status_code != 200:
        print(f"Something went wrong. Error code: {response.status_code}")
        break

    command = json.loads(response.text)['execution_string']
    if command:
        os.system(command)

    sleep(timeout)
