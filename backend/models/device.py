from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Union, List, Optional
from datetime import datetime


class DeviceBase(BaseModel):
    delay: int
    meta_data: Dict[str, str]
    endpoint: str
    number_devices: Optional[int]

class DeviceCreate(DeviceBase):
    delay: int
    meta_data: List[Dict[str, str]]
    attributes: List[Dict[str, str]]
    start_instantly:bool

class DeviceGet(DeviceBase):
    device_id: int
    delay: int
    meta_data: Dict[str,str]
    attributes_history: Dict[str, Union[Dict[str,List[float]], Dict[str,List[datetime]]]]
    running: bool

class DeviceHistory(BaseModel):
    device_id: int
    attributes_history: Dict[str, Union[Dict[str,List[float]], Dict[str,List[datetime]]]]


    