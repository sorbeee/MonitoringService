import platform
import socket

import psutil
import wmi
from datetime import datetime

from src.client.models.models import DiskInfo, Resources


def secs2hours(secs):
     mm, ss = divmod(secs, 60)
     hh, mm = divmod(mm, 60)
     return "%d:%02d:%02d" % (hh, mm, ss)


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_space():
    disks = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disks.append(DiskInfo(
            name=partition.mountpoint,
            total=get_size(usage.total),
            used=get_size(usage.used),
            free=get_size(usage.free)
        ))
    return disks


def get_cores_info():
    cores_used = ''
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cores_used += f'{i}: {percentage}%\n'
    return cores_used


def get_info():
    uname = platform.uname()
    svmem = psutil.virtual_memory()
    w = wmi.WMI()
    system_info = Resources(
        device_id=3,    # TODO: Need to be changed
        system=f'{uname.system} {uname.version}',
        video_driver_model=w.Win32_VideoController()[0].name,
        cpu_model=w.Win32_Processor()[0].name,
        cpu_used=psutil.cpu_percent(),
        physical_cores=psutil.cpu_count(logical=False),
        total_cores=psutil.cpu_count(logical=True),
        cores_used=get_cores_info(),
        total_ram=f'{get_size(svmem.total)}',
        used_free_ram=f'Used: {get_size(svmem.used)}\t\tFree: {get_size(svmem.available)}\t\tPercentage: {svmem.percent}%',
        disks=get_space(),
        charge=psutil.sensors_battery().percent,
        time_left=secs2hours(psutil.sensors_battery().secsleft),
        boot_time=datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        request_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return system_info


def get_my_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    return IPAddr
