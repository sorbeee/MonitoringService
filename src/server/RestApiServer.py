import threading
import io

from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from starlette.responses import StreamingResponse

from models.response_models import *
from utils import *

app = FastAPI()


@app.get("/resources/{device_id}", response_model=List[DeviceResources])
async def get_all_resources(device_id: int, limit: int):
    return convert_resource_data(select_all_resources(device_id, limit), device_id)


@app.get("/device", response_model=List[Device])
async def get_all_devices():
    return convert_device_data(select_all_devices())


@app.get("/activity", response_model=List[Activity])
async def get_all_activity():
    return convert_activity_data(select_all_activity())


@app.get("/")
async def home_page():
    return RedirectResponse("http://127.0.0.1:3000/docs")


@app.get("/activity/{device_id}", response_model=DeviceActivity)
async def get_activity_by_id(device_id: int):
    item = select_activity(device_id)[0]
    response = {
        "device_id": item[0],
        "is_online": item[1],
        "last_ping": item[2],
        "last_time_online": item[3]
    }
    return response


@app.get("/action/{device_id}", response_model=Action)
async def get_action(device_id: int, system: str):
    action = select_action(device_id, system)
    response = {}
    if action:
        response = {
          "execution_string": select_action(device_id, system)[0][0]
        }
        remove_action(device_id)

    return response


@app.get("/action", response_model=List[AvailableAction])
async def get_all_available_actions():
    return convert_action_data(select_all_actions())


@app.get("/stat/{device_id}")
async def get_stat(device_id: int, stat_type: str, interval: str):
    data = select_stat(device_id, stat_type, interval)
    stat_chart = None
    if len(data) < 2:
        raise HTTPException(status_code=418, detail="Not enough information")
    else:
        if stat_type == 'disks':
            stat_chart = create_disk_stat(data)
        elif stat_type == 'charge':
            stat_chart = create_charge_stat(data)
        elif stat_type == 'used_free_ram':
            stat_chart = create_ram_stat(data)
        elif stat_type == 'cpu_used':
            stat_chart = create_cpu_stat(data)

        buffer = io.BytesIO()
        stat_chart.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return StreamingResponse(io.BytesIO(buffer.read()), media_type="image/png")


@app.post("/device", response_model=ResponseModel)
async def create_device(device: Device):
    if not insert_device(device.name, device.ip, device.notification):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return {"status": 200}


@app.post("/activity", response_model=ResponseModel)
async def insert_device_activity(activity: DeviceActivity):
    if not insert_activity(activity.device_id, activity.is_online, activity.last_ping, activity.last_time_online):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return {"status": 200}


@app.post("/resources", response_model=ResponseModel)
async def add_resources(resources: Resources):
    if store_info(resources) != True:
        raise HTTPException(status_code=400, detail="Invalid device ID")
    return {"status": 200}


@app.post("/action", response_model=ResponseModel)
async def insert_device_actions(action: ActionList):
    if not insert_action(action.device_id, action.action_id):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return {"status": 200}


@app.put("/device/{device_id}", response_model=ResponseModel)
async def update_device_fields(device_id: int, notifications: bool):
    if not update_device(device_id, notifications):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return {"status": 204}


@app.put("/activity/{device_id}", response_model=ResponseModel)
async def update_action_fields(device_id: int, activity_id: int):
    if not update_action(device_id, activity_id):
        raise HTTPException(status_code=400, detail="An error occurred on the database side")
    return {"status": 200}


@app.delete("/device/{device_id}", response_model=ResponseModel)
async def delete_device(device_id: int):
    if not remove_device(device_id):
        raise HTTPException(status_code=400, detail="Invalid device ID")
    return {"status": 204}


@app.delete("/action/{action_id}", response_model=ResponseModel)
async def delete_action(action_id: int):
    if not remove_action(action_id):
        raise HTTPException(status_code=400, detail="Invalid action ID")
    return {"status": 204}


@app.on_event("startup")
async def startup_event():
    start_db()
    #ping_thread = threading.Thread(target=lambda: start_ping(15))
    #notification_thread = threading.Thread(target=send_notification)

    #ping_thread.start()
    #notification_thread.start()
