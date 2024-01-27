from typing import List

from fastapi import FastAPI, HTTPException
from db_scripts import *
from models.response_models import *
from utils import store_info, convert_device_data, convert_activity_data, convert_resource_data

app = FastAPI()


@app.get("/resources/{device_id}", response_model=List[DeviceResources])
def get_all_resources(device_id: int):
    start_db()
    return convert_resource_data(select_all_resources(device_id), device_id)


@app.get("/device", response_model=List[Device])
def get_all_devices():
    start_db()
    return convert_device_data(select_all_devices())


@app.get("/activity", response_model=List[Activity])
def get_all_activity():
    start_db()
    return convert_activity_data(select_all_activity())


@app.get("/activity/{device_id}", response_model=DeviceActivity)
def get_activity_by_id(device_id: int):
    start_db()
    item = select_activity(device_id)[0]
    response = {
        "device_id": item[0],
        "is_online": item[1],
        "last_ping": item[2],
        "last_time_online": item[3]
    }
    return response


@app.get("/actions/{device_id}")
def get_action(device_id: int, system: str):
    start_db()
    return select_action(device_id, system)


@app.post("/device")
def create_device(device: Device):
    start_db()
    if not insert_device(device.name, device.ip, device.notification):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return 200


@app.post("/activity")
def insert_device_activity(activity: DeviceActivity):
    start_db()
    if not insert_activity(activity.device_id, activity.is_online, activity.last_ping, activity.last_time_online):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return 200


@app.post("/resources", response_model=ResponseModel)
def add_resources(resources: Resources):
    if store_info(resources) != True:
        raise HTTPException(status_code=400, detail="Invalid device ID")
    return {"response": 200}


@app.put("/device/{device_id}")
def update_device_fields(device_id: int, notifications: bool):
    start_db()
    if not update_device(device_id, notifications):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return 200


@app.put("/activity/{device_id}", response_model=ResponseModel)
def update_action_fields(device_id: int, activity_id: int):
    start_db()
    if not update_action(device_id, activity_id):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return 200


@app.delete("/device/{device_id}")
def delete_device(device_id: int):
    start_db()
    if not remove_device(device_id):
        raise HTTPException(status_code=400, detail="Invalid device ID")
    return {"status": 204}


@app.delete("/action/{action_id}", response_model=ResponseModel)
def delete_action(action_id: int):
    start_db()
    if not remove_action(action_id):
        raise HTTPException(status_code=400, detail="Invalid action ID")
    return {"status": 204}



# @app.on_event("startup")
# async def startup_event():
#     start_db()
#     ping_thread = threading.Thread(target=lambda: start_ping(15))
#     notification_thread = threading.Thread(target=send_notification)
#
#     ping_thread.start()
#     notification_thread.start()
