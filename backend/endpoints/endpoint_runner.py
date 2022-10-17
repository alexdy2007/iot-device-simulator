import threading
import asyncio
import logging
import sys

from endpoints.endpoint import EndPoint
from typing import List
from queue import Queue


class EndpointRunner(threading.Thread):

    def __init__(self, initial_endpoints:List[EndPoint], device_reading_queue:Queue):

        super().__init__()

        self.setDaemon(True)
        self.device_reading_queue=device_reading_queue
        self.initial_endpoints = []
        self._endpoints = {e.id:{'task': None, 'endpoint':e} for e in initial_endpoints}

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



    def add_endpoint(self, endpoint:EndPoint):
        self._endpoints[endpoint.id] = {'task': None, 'endpoint':endpoint}
        # self.start_endpoint(endpoint.id)

    def get_all_endpoints(self):
         return [e['endpoint'] for e in self._endpoints.values()]


    def get_endpoint_by_id(self, id):
        return [e for e in self._endpoints.values() if e.id==id][0]


    def run(self):
    
        asyncio.set_event_loop(self.loop)

        if __debug__:
            self.loop.set_debug(True)

        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()     


