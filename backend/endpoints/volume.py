from typing import Any, List, Dict
from endpoints.endpoint import EndPoint
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import datetime
import logging
import json
import io
from databricks.sdk import WorkspaceClient
import uuid

from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class VolumeEndpoint(EndPoint):

    def __init__(self, name:str, volume_path:str, workspace_client:WorkspaceClient=None, delay=10) -> None:
        self.name = name
        self.volume_path = volume_path
        self.workspace_client = workspace_client
        super().__init__(name, delay=delay)


    def json_format(self):
        return {
            "name":self.name,
            "path":self.volume_path,
            "id": self.id
        }


    async def send(self, messages:List[Dict[str,Any]], file_name:str=None):

        if file_name is None:
            file_name = str(uuid.uuid4()) + ".json"
        

        try:
            messages_json = json.dumps(messages, default=json_serial)
            messages_json_bytes = messages_json.encode('utf-8')
            byte_buffer = io.BytesIO(messages_json_bytes)
            self.workspace_client.files.upload(f"{self.volume_path}/{file_name}", byte_buffer, overwrite=True)
        except Exception as e:
            self.logger.error(f'error sending messages to {self.volume_path}/{file_name} {e}')


    async def start(self):
        self.logger.debug(f'endpoint {self.id} started')
        self.running=True
        while self.running==True:
            messages = [self.messages_to_send.pop() for _ in range(40) if self.messages_to_send]
            self.logger.info(f'length of {len(messages)} messages')
            if len(messages)!=0:
                await self.send(messages)
                self.messages_to_send = []
            await asyncio.sleep(self.delay)


