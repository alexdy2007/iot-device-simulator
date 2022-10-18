from email import message
import threading
import asyncio
import logging
import sys

from endpoints.endpoint import EndPoint
from typing import List, Dict, Any
from queue import Queue
from datetime import datetime


class EndpointRunner(threading.Thread):

    def __init__(self, initial_endpoints:List[EndPoint], device_reading_queue:Queue, collect_messages_sync:float=0.5):

        super().__init__()

        self.setDaemon(True)
        self.device_reading_queue=device_reading_queue
        self.initial_endpoints = initial_endpoints
        self.collect_messages_sync = collect_messages_sync
        self.logger = self.create_logger()
        self.loop = asyncio.new_event_loop()
        self.collect_message_task = None
        self._endpoints = {e.id:{'task': None, 'endpoint':e} for e in initial_endpoints}
        self.start()

    @staticmethod
    def create_logger():
        h1 = logging.StreamHandler(sys.stdout)
        if __debug__:
            h1.setLevel(logging.DEBUG)
        else:
            h1.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        h1.setFormatter(formatter)
        logger = logging.getLogger('EndpointRunner')
        return logger

    async def collect_messages(self):
        while self.collect_message_task!=None:
            while self.device_reading_queue.empty()==False:
                message = self.device_reading_queue.get()
                endpoint = self.get_endpoint(message['endpoint_id'])
                endpoint.add_message(message)
            
            await asyncio.sleep(self.collect_messages_sync)

    def start_collect_messages(self):
        if self.collect_message_task==None:
            future = asyncio.run_coroutine_threadsafe(self.collect_messages(), self.loop)
            self.collect_message_task = future

    def add_endpoint(self, endpoint:EndPoint):
        self._endpoints[endpoint.id] = {'task': None, 'endpoint':endpoint}
        # self.start_endpoint(endpoint.id)

    def get_all_endpoints(self) -> List[EndPoint]:
         return [e['endpoint'] for e in self._endpoints.values()]


    def get_endpoint(self, endpoint_id:int) -> EndPoint:
        endpoint = self._endpoints.get(endpoint_id, {}).get('endpoint', None)
        if endpoint == None:
            self.logger.error(f'Endpoint not found with id {endpoint_id}')
            raise KeyError(f'Endpoint not found with id {endpoint_id}')
        return endpoint

    def get_endpoint_item(self, endpoint_id:int) -> Dict[str, Any]:
        endpoint_item = self._endpoints.get(endpoint_id, None)
        if endpoint_item == None:
            self.logger.error(f'Endpoint not found with id {endpoint_item}')
            raise KeyError(f'Endpoint not found with id {endpoint_item}')
        return endpoint_item    

    def is_endpoint_running(self, endpoint_id:int) -> bool:
        try:
            endpoint_item = self.get_endpoint_item(endpoint_id)
        except KeyError:
            return False

        return endpoint_item['task']!=None

    def start_endpoint(self, endpoint_id:int) -> bool:

        if self.is_endpoint_running(endpoint_id)==True:
            self.logger.warning('endpoint: {endpoint_id} already running')
            return False
        try:
            endpoint = self.get_endpoint(endpoint_id)
        except KeyError:
            return False
        future = asyncio.run_coroutine_threadsafe(endpoint.start(), self.loop)
        self._endpoints[endpoint.id]['task'] = future 
        return True

    def start_all_endpoints(self):

        self.logger.debug(f'Starting all endpoints')
        for endpoint_id in self._endpoints.keys():
            self.start_endpoint(endpoint_id)

    def stop_all_endpoints(self):
        self.logger.debug(f'Stopping all endpoints')

        for endpoint_id in self._endpoints.keys():
            self.stop_endpoint(endpoint_id)


    def stop_endpoint(self, endpoint_id:int):

        if self.is_endpoint_running(endpoint_id)==False:
            self.logger.debug(f'Endpoint {endpoint_id} already stoped, cant stop')
            return False
        try:
            endpoint_task = self.get_endpoint_item(endpoint_id)
            self.logger.info(f'Stopping Endpoint with ID {endpoint_id}')
            self._endpoints[endpoint_id]['endpoint'].stop()
            self.loop.call_soon_threadsafe(endpoint_task['task'].cancel)
            self._endpoints[endpoint_id]['task'] = None
        except KeyError:
            pass
     
        return True

    def get_endpoint_by_id(self, endpoint_id:int) -> EndPoint:
        return [e for e in self._endpoints.values() if e.id==endpoint_id][0]


    def run(self):
        self.logger.debug('starting endpoint runner')
        asyncio.set_event_loop(self.loop)

        if __debug__:
            self.loop.set_debug(True)

        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()     


