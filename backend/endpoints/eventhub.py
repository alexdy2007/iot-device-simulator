from typing import Any, List, Dict
from endpoints.endpoint import EndPoint
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import datetime
import logging
import json

class EventhubEndpoint(EndPoint):

    def __init__(self, name:str, connection_string:str, eventhub_name:str, delay:int=1) -> None:
        self.connection_string = connection_string
        self.eventhub_name = eventhub_name
        self.device_client = self.get_device_clint()
        super().__init__(name, delay=delay)
        logging.getLogger("uamqp").setLevel(logging.CRITICAL)  # Low level uAMQP are logged only for critical
        logging.getLogger("azure").setLevel(logging.CRITICAL)  # All azure clients are logged only for critical


    def json_format(self):
        return {
            "name":self.name,
            "connection_string":self.connection_string,
            "id": self.id
        }

    def get_device_clint(self):
        device_client = EventHubProducerClient.from_connection_string(conn_str=self.connection_string, eventhub_name=self.eventhub_name, websockets=True)
        return device_client

    async def send(self, messages:List[Dict[str,Any]]):
 

        # Create a batch.
        try:
            async with self.device_client:

                event_data_batch = await self.device_client.create_batch()
                # Add events to the batch.
                print(len(messages))
                for message in messages:
                    message['time'] = message['time'].isoformat()
                    print(message)
                    json_message = json.dumps(message)
                    event_data_batch.add(EventData(json_message))
                # Send the batch of events to the event hub.
                await self.device_client.send_batch(event_data_batch)
        except Exception as e:
            self.logger.error(f"SOMETHING WENT WRONG SENDING TO EVENTHUB {e}")
        return 


    async def start(self):
        self.logger.debug(f'endpoint {self.id} started')
        self.running=True
        while self.running==True:
            messages = [self.messages_to_send.pop() for _ in range(40) if self.messages_to_send]
            if len(messages)!=0:
                await self.send(messages)
                self.messages_to_send = []
            await asyncio.sleep(self.delay)


