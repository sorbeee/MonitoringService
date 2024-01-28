import datetime

from pydantic import BaseModel


class Device(BaseModel):
    id: int = None
    name: str
    ip: str
    notification: bool


class Activity(BaseModel):
    device_name: str
    device_ip: str
    is_online: bool
    last_time_online: datetime.datetime
    notification: bool


class DeviceActivity(BaseModel):
    device_id: int
    is_online: bool
    last_ping: datetime.datetime
    last_time_online: datetime.datetime


class Resources(BaseModel):
    device_id: int = None
    system: str
    video_driver_model: str
    cpu_model: str
    cpu_used: float
    physical_cores: int
    total_cores: int
    cores_used: str
    total_ram: str
    used_free_ram: str
    disks: list
    charge: int
    time_left: str
    boot_time: datetime.datetime
    request_time: datetime.datetime


class DeviceResources(Resources):
    device_name: str
    device_ip: str


class ResponseModel(BaseModel):
    status: int


class Action(BaseModel):
    execution_string: str = None
