from pydantic import BaseModel
from typing import Optional

class EndpointBase(BaseModel):
    Optional[id]:int
    name:str
    endpoint_type:str

class EventHubModel(EndpointBase):
    connection_string:str
    eventhub_name:str