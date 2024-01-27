import datetime
import time
import requests
import os
from SQLScripts.db_scripts import *


def ping(ip_address, count=5, timeout=5):
    response = os.system("ping -n %d -w %d %s" % (count, timeout, ip_address))
    return response == 0


def execute_ping():
    devices = select_ips()
    for info in devices:
        is_online = ping(info[1])
        current_time = datetime.datetime.now()
        last_activity = select_activity(info[0])
        if last_activity:
            if is_online:
                update_activity(last_activity[0][0], is_online, current_time, current_time)
            elif is_online == False and last_activity[0][1] == True:
                update_activity(last_activity[0][0], is_online, current_time, last_activity[0][2])
            elif is_online == False and last_activity[0][1] == False:
                update_activity(last_activity[0][0], is_online, current_time, last_activity[0][3])
        else:
            insert_activity(info[0], is_online, current_time, current_time)


def send_notification():
    config = read_json(config_path)["TELEGRAM_BOT"]
    while True:
        if config["NOTIFICATIONS"]:
            BOT_TOKEN = config["BOT_TOKEN"]
            CHAT_ID = config["CHAT_ID"]
            previous_activity = select_all_activity()
            time.sleep(35)
            current_activity = select_all_activity()
            for prev, curr in zip(previous_activity, current_activity):
                if prev[4] and prev[2] and not curr[2]:
                    message = f'!!!\tName:{prev[0]}\t\tIP:{prev[1]}\t\tis offline!!!'
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
                    requests.get(url).json()
        else:
            time.sleep(10)
            continue


def store_info(msg):
    return insert_resources(msg.device_id,
                            msg.system,
                            msg.video_driver_model,
                            msg.cpu_model,
                            msg.cpu_used,
                            msg.physical_cores,
                            msg.total_cores,
                            msg.cores_used,
                            msg.total_ram,
                            msg.used_free_ram,
                            msg.disks,
                            msg.charge,
                            msg.time_left,
                            msg.boot_time,
                            msg.request_time
                            )


def start_ping(timeout):
    while True:
        execute_ping()
        time.sleep(timeout)


def convert_device_data(input_data):
    output_data = []
    for item in input_data:
        converted_item = {
            "id": item[0],
            "name": item[1],
            "ip": item[2],
            "notification": item[3]
        }
        output_data.append(converted_item)
    return output_data


def convert_activity_data(input_data):
    output_data = []
    for item in input_data:
        converted_item = {
            "device_name": item[0],
            "device_ip": item[1],
            "is_online": item[2],
            "last_time_online": item[3],
            "notification": item[4]
        }
        output_data.append(converted_item)
    return output_data
