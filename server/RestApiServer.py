from typing import List

from fastapi import FastAPI, HTTPException
from SQLScripts.db_scripts import *
from response_models import *
from utils import store_info, convert_device_data, convert_activity_data

app = FastAPI()

@app.get("/resources", response_model=List[Resources])
def get_all_resources():
    pass


@app.get("/device", response_model=List[Device])
def get_all_devices():
    start_db()
    return convert_device_data(select_all_devices())


@app.delete("/device/{device_id}")
def delete_device(device_id: int):
    start_db()
    if not remove_device(device_id):
        raise HTTPException(status_code=400, detail="Invalid device ID")
    return {"status": 204}


@app.put("/device/{device_id}")
def update_device_fields(device_id: int, notifications: bool):
    start_db()
    if not update_device(device_id, notifications):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return 200


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


@app.get("/actions/{device_id}", response_model=Action)
def get_action(device_id: int):
    pass


@app.post("/resources")
def add_resources(resources: Resources):
    if store_info(resources) != True:
        raise HTTPException(status_code=400, detail="Invalid device ID")
    return {"response": 200}




# @app.on_event("startup")
# async def startup_event():
#     start_db()
#     ping_thread = threading.Thread(target=lambda: start_ping(15))
#     notification_thread = threading.Thread(target=send_notification)
#
#     ping_thread.start()
#     notification_thread.start()
