import datetime

from pydantic import BaseModel


class Device(BaseModel):
    id: int
    name: str
    ip: str
    notification: bool


class Activity(BaseModel):
    device_name: str
    device_ip: str
    is_online: bool
    last_time_online: datetime.datetime
    notification: bool


class Resources(BaseModel):
    device_id: int
    system: str
    video_driver_model: str
    cpu_model: str
    cpu_used: str
    physical_cores: int
    total_cores: int
    cores_used: str
    total_ram: str
    used_free_ram: str
    disks: str
    charge: str
    time_left: str
    boot_time: datetime.datetime
    request_time: datetime.datetime


class Action(BaseModel):
    id: int
    name: str
    execution_string: str


class DeviceActivity(BaseModel):
    device_id: int
    is_online: bool
    last_ping: datetime.datetime
    last_time_online: datetime.datetime