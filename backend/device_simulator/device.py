import asyncio
import logging
import sys

from typing import Dict, Any
from collections import deque
from datetime import datetime
from pprint import pprint

import calendar

from device_simulator.distributions import Distribution

class Device():

    count=0

    @classmethod
    def gen_id(cls):
        while True:
            cls.count = cls.count+1
            yield cls.count

    def __init__(self, delay:int=10, attributes:Dict[str, Distribution]=None, meta_data:Dict[str,str] = None, max_history:int=30, endpoint_id:int=1, device_reading_queue=None):
        self.device_id = next(self.gen_id())
        self.delay=delay
        self.meta_data = meta_data
        self.attributes = attributes
        self.endpoint_id = endpoint_id
        self.logger = self.create_logger()
        self.running = False

        self.task = None
        self.device_reading_queue=device_reading_queue

        self.attributes_history = {}
        for attribute_name in attributes.keys():
            self.attributes_history[attribute_name] = deque(maxlen=max_history)

    def get_device_info(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "delay": self.delay,
            'endpoint': self.endpoint_id,
            "meta_data": self.meta_data,
            "attributes": [{'name': k, 'model':v.get_info()} for k,v in self.attributes.items()],
            'running': self.running
        }
        

    def create_logger(self):
        h1 = logging.StreamHandler(sys.stdout)
        if __debug__:
            h1.setLevel(logging.DEBUG)
        else:
            h1.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        h1.setFormatter(formatter)
        logger = logging.getLogger(f'Device_{self.device_id}')
        return logger


    async def start(self):
        self.logger.debug(f'device {self.device_id} Started')
        self.running=True
        while self.running==True:
            for attribute_name, generator in self.attributes.items():
                time_stamp = calendar.timegm(datetime.now().timetuple())
                value = {'device_id':self.device_id, 'attribute':attribute_name, 'time':datetime.now(), "unixtime":time_stamp, 'value':round(generator.generate_value()[0],2), "endpoint_id":self.endpoint_id}
                self.attributes_history[attribute_name].append(value)
                self.device_reading_queue.put(value)
            await asyncio.sleep(self.delay)

    def stop(self):
        self.running=False

    def print_historic_values(self):
        pprint(self.attributes_history)

    def get_last_n_readings(self, n:int):
        last_n_readings = {}
        for k,d in self.attributes_history.items():
            last_n_readings[k] = list(d)[-n:]
        return last_n_readings

    def add_attribute(self, name:str, distribution:Distribution):
        return NotImplementedError

    def add_metadata(self, name:str, value):
        return NotImplementedError   

