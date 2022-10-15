import logging

from typing import Union
from fastapi import FastAPI, HTTPException, Response
from device_simulator.device_runner import DeviceRunner
from device_simulator.device import Device, create_dummy_device
from app.models.Device import DeviceCreate

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger

from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device_starter_1 = create_dummy_device(delay=5)
device_starter_2 = create_dummy_device(location='Horsforth Pumping')
device_starter_3 = create_dummy_device(delay=20, location='Harrogate Sewage Treatment')

device_sim = DeviceRunner([device_starter_1, device_starter_2, device_starter_3])

@app.on_event("startup")
async def startup_event():

    device_sim.start_all_devices()

@app.on_event("shutdown")
def shutdown_event():
    if device_sim != None:
        device_sim.stop_runner()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/devices")
async def create_device(device: DeviceCreate):
    raise HTTPException(status_code=501, detail='Not Implemented Yet')

@app.get("/devices/{device_id}")
def get_device(device_id:int):

   

    device = device_sim.get_device(device_id)
    device_info = device.get_device_info()

    headers = {
        "Access-Control-Allow-Private-Network": "true"
    }
    response = JSONResponse(
        headers=headers,
        content=device_info
    )

    return response

@app.get("/devices")
def get_devices():
    devices = device_sim.get_all_devices()
    devices_info = [d.get_device_info() for d in devices]
    return devices_info

@app.get("/devices/readings/{device_id}")
def get_device_reading(device_id:int, n_historic:int=10):
    try:
        device_history = device_sim.get_last_n_readings_from_device(device_id, n_historic)
    except KeyError:
        detail = f"Device {device_id} not found"
        return HTTPException(status_code=404, detail=detail)
    return device_history


@app.get("/devices/pause/{device_id}")
def pause_device(device_id:int):
    try:
        device_status = device_sim.stop_device(device_id)
    except KeyError:
        detail = f"Device {device_id} not found"
        return HTTPException(status_code=404, detail=detail)
    
    headers = {
        "Access-Control-Allow-Private-Network": "true"
    }
    if device_status==False:
        return HTTPException(status_code=409, detail='Device Already Paused')

    response = JSONResponse(
        headers=headers,
        content={"detail":'Device Paused'}
    )

    return response

@app.get("/devices/start/{device_id}")
def start_device(device_id:int):
    try:
        device_status = device_sim.start_device(device_id)
    except KeyError:
        detail = f"Device {device_id} not found"
        return HTTPException(status_code=404, detail=detail)
    
    headers = {
        "Access-Control-Allow-Private-Network": "true"
    }

    if device_status==False:
        return HTTPException(status_code=409, detail='Device Already Started')

    response = JSONResponse(
        headers=headers,
        content={"detail":'Device Started'}
    )

    return response