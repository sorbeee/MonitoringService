import datetime
import json
import os
from db_scripts import *

import matplotlib

def ping(ip_address, count=5, timeout=5):
    response = os.system("ping -n %d -w %d %s" % (count, timeout, ip_address))
    return response == 0


def execute_ping():
    devices = select_ips()
    for info in devices:
        is_online = ping(info[1])
        time = datetime.datetime.now()
        last_activity = select_activity(info[0])
        if last_activity:
            if is_online:
                update_activity(last_activity[0][0], is_online, time, time)
            elif is_online == False and last_activity[0][1] == True:
                update_activity(last_activity[0][0], is_online, time, last_activity[0][2])
            elif is_online == False and last_activity[0][1] == False:
                update_activity(last_activity[0][0], is_online, time, last_activity[0][3])
        else:
            insert_activity(info[0], is_online, time, time)


def store_info(msg):
    data = json.loads(msg)
    disks = ''

    for el in data['disks']:
        disks += el['name'] + '\ttotal: ' + el['total'] + '\tused: ' + el['used'] + '\tfree:' + el['free'] + '\n'
    insert_resources(data['device_id'],
                     data['system'],
                     data['video_driver_model'],
                     data['cpu_model'],
                     data['cpu_used'],
                     data['physical_cores'],
                     data['total_cores'],
                     data['cores_used'],
                     data['total_ram'],
                     data['used_free_ram'],
                     disks,
                     data['charge'],
                     data['time_left'],
                     data['boot_time'],
                     data['request_time']
                     )
