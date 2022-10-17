import logging

from typing import Union
from fastapi import FastAPI, HTTPException, Response
from device_simulator.device_runner import DeviceRunner
from device_simulator.device import Device
from app.models.device import DeviceCreate

from device_simulator.test.stubs import create_dummy_device

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as fastapi_logger

from fastapi.middleware.cors import CORSMiddleware

from device_simulator.distributions import BetaDist, NormalDist

from endpoints.endpoint_runner import EndpointRunner
from endpoints.eventhub import EventhubConfig
from endpoints.nullendpoint import NullEndpointConfig

from app.models.endpoints import EventHubModel

import queue

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

device_reading_queue = queue.Queue()
device_sim = DeviceRunner([device_starter_1, device_starter_2, device_starter_3], device_reading_queue=device_reading_queue)

null_endpoint = NullEndpointConfig()
endpoint_store = EndpointRunner([null_endpoint], device_reading_queue)

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

@app.post("/devices", status_code=201)
async def create_device(device: DeviceCreate):

   
    attributes = {}
    meta_data = {}

    for attribute in device.attributes:
        name = attribute['name']
        if attribute['model'] == 'Normal':
            mean = int(attribute['mean'])
            sd = int(attribute['sd'])
            attributes[name] = NormalDist(mean=mean, sd=sd)
        elif attribute['model'] == 'Beta':
            beta_a = int(attribute['beta_a'])
            beta_b = int(attribute['beta_b'])
            scale = int(attribute['scale'])
            attributes[name] = BetaDist(a=beta_a, b=beta_b, scale=scale)
        else:
            msg = f"Model of type {attribute['model']} not implmented"
            raise HTTPException(status_code=501, detail=msg)

    for meta in device.meta_data:
        key = meta['key']
        value = meta['value']
        meta_data[key] = value
    
    delay = device.delay
    endpoint_id = device.endpoint

    number_devices = int(device.number_devices)

    for _ in range(number_devices):
        device = Device(delay=delay, attributes=attributes, meta_data=meta_data, endpoint_id=endpoint_id, device_reading_queue=device_reading_queue)
        device_sim.add_device(device)
        
    headers = {
        "Access-Control-Allow-Private-Network": "true"
    }

    msg = f"{number_devices} Devices created and started"

    response = JSONResponse(
        headers=headers,
        content={"detail": msg}
    )
    return response

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

@app.delete("/devices", status_code=200)
def delete_all_devices():
    device_sim.remove_all_devices()
    
    headers = {
        "Access-Control-Allow-Private-Network": "true"
    }
   
    response = JSONResponse(
        headers=headers,
        content={"detail":'All Devices Deleted'}
    )
    
    return response 


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

@app.get("/endpoints/")
def get_all_endpoints():

    response_data = [x.json_format() for x in endpoint_store.get_all_endpoints()]
    
    print(response_data)


    headers = {
        "Access-Control-Allow-Private-Network": "true"
    }
    response = JSONResponse(
        headers=headers,
        content=response_data
    )

    return response

@app.get("/endpoints/{endpoint_id}")
def get_endpoint(endpoint_id:int):

    endpoint = endpoint_store.get_endpoint_by_id(endpoint_id)
    response_data = endpoint.json_format()

    headers = {
        "Access-Control-Allow-Private-Network": "true"
    }
    response = JSONResponse(
        headers=headers,
        content=response_data
    )

    return response

@app.post("/endpoints/", status_code=201)
async def create_endpont(endpoint: EventHubModel):

    if endpoint.endpoint_type=='EventHub':
        endpoint_model = EventhubConfig(name=endpoint.name, connection_string=endpoint.connection_string)
    else:
        detail = f"Endpoint type {endpoint.endpoint_type} not reconised"
        return HTTPException(status_code=404, detail=detail)
    

    endpoint_store.add_endpoint(endpoint_model)   
    headers = {
        "Access-Control-Allow-Private-Network": "true"
    }

    msg = f"added endpoint {endpoint_model.name}"
    response = JSONResponse(
        headers=headers,
        content={"detail": msg}
    )
    return response
    
