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

class VolumeEndpoint(EndPoint):

    def __init__(self, name:str, volume_path:str, workspace_client:WorkspaceClient=None, delay=20) -> None:
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
        string_buffer = io.StringIO()

        if file_name is None:
            file_name = str(uuid.uuid4()) + ".json"

        for message in messages:
            message['time'] = message['time'].isoformat()
            print(message)
            json.dump(message, string_buffer)

        byte_buffer = io.BytesIO(string_buffer.getvalue().encode('utf-8'))
        self.workspace_client.files.upload(f"{self.volume_path}/{file_name}", byte_buffer, overwrite=True)


    async def start(self):
        self.logger.debug(f'endpoint {self.id} started')
        self.running=True
        while self.running==True:
            messages = [self.messages_to_send.pop() for _ in range(40) if self.messages_to_send]
            if len(messages)!=0:
                await self.send(messages)
                self.messages_to_send = []
            await asyncio.sleep(self.delay)


