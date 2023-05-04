import psutil
import wmi
from datetime import datetime

def secs2hours(secs):
     mm, ss = divmod(secs, 60)
     hh, mm = divmod(mm, 60)
     return "%d:%02d:%02d" % (hh, mm, ss)


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def getSpace():
    disks = []
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        disks.append({
            "name": partition.mountpoint,
            "total": toFixed(usage.total / pow(1024, 3), 3),
            "used": toFixed(usage.used / pow(1024, 3), 3),
            "free": toFixed(usage.free / pow(1024, 3), 3)})
    return disks

def getInfo():
    w = wmi.WMI()
    system_info = {
        "device_id": 1,
        "cpu_used": psutil.cpu_percent(),
        "memory_used": psutil.virtual_memory().percent,
        "cpu_model": w.Win32_Processor()[0].NumberOfCores,
        "cpu_cores": w.Win32_Processor()[0].NumberOfCores,
        "video_driver_model": w.Win32_VideoController()[0].name,
        "disks": getSpace(),
        "charge": psutil.sensors_battery().percent,
        "time_left": secs2hours(psutil.sensors_battery().secsleft),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "request_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }
    return system_info
