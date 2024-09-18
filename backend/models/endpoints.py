from pydantic import BaseModel, Field
from typing import Optional, Union

class EndpointBase(BaseModel):
    id: Union[int,None] = Field(default=None)
    name:str
    endpoint_type:str
    delay:int = Field(
        default=10,
    )

class EventHubModel(EndpointBase):
    connection_string:str
    eventhub_name:str

class VolumeModel(EndpointBase):
    volume_path:str
    connection_string:str
    eventhub_name:str