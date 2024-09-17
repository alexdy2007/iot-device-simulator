import logging
import sys
import asyncio
from collections import deque


def gen_id():
    count = 0 
    while True:
        count = count+1
        yield count

class EndPoint():

    id_gen = gen_id()

    def __init__(self, name:str, delay=1):
        self.id = next(self.id_gen)
        self.name = name
        self.messages_to_send = deque()
        self.delay=delay
        self.logger = self.create_logger()
        self.running = False
        self.logger.debug(f'endpoint {self.id} created of type {self.__class__.__name__}')
    
    def create_logger(self):
        h1 = logging.StreamHandler(sys.stdout)
        if __debug__:
            h1.setLevel(logging.DEBUG)
        else:
            h1.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        h1.setFormatter(formatter)
        logger = logging.getLogger(f'Endpoint_{self.id}')
        return logger

    def add_message(self, message):
        self.messages_to_send.append(message)

    async def start(self):
        return NotImplementedError

    def stop(self):
        self.running=False

    def send(message):
        return NotImplementedError

    def json_format():
        return NotImplementedError

    
