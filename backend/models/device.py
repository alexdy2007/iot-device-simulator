from pydantic import BaseModel
from typing import Dict, Union, List, Optional
from datetime import datetime


class DeviceBase(BaseModel):
    delay: Union[str, int]
    meta_data: Dict[str, str]
    endpoint: Union[str, int]
    number_devices: Optional[int]

class DeviceCreate(DeviceBase):
    delay: int
    meta_data: List[Dict[str, Union[str, int]]]
    attributes: List[Dict[str, Union[str, int]]]
    start_instantly:bool

class DeviceGet(DeviceBase):
    device_id: int
    delay: Union[str, int]
    meta_data: Dict[str,Union[str, int]]
    attributes_history: Dict[str, Union[Dict[str,List[float]], Dict[str,List[datetime]]]]
    running: bool

class DeviceHistory(BaseModel):
    device_id: int
    attributes_history: Dict[str, Union[Dict[str,List[float]], Dict[str,List[datetime]]]]


    