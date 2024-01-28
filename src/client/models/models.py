import datetime

from pydantic.v1 import BaseModel


class DiskInfo(BaseModel):
    name: str
    total: str
    used: str
    free: str


class Resources(BaseModel):
    device_id: int
    system: str
    video_driver_model: str
    cpu_model: str
    cpu_used: float
    physical_cores: int
    total_cores: int
    cores_used: str
    total_ram: str
    used_free_ram: str
    disks: list[DiskInfo]
    charge: int
    time_left: str
    boot_time: datetime.datetime
    request_time: datetime.datetime
