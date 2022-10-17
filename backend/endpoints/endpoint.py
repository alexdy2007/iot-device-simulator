import logging
import sys
import asyncio

class EndPoint():

    count = 0

    @classmethod
    def gen_id(cls):
        while True:
            cls.count = cls.count+1
            yield cls.count

    def __init__(self, name, delay=1):
        self.id = next(self.gen_id())
        self.name = name
        self.messages_to_send = []
        self.delay=delay
        self.logger = self.create_logger()
        self.running = False

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


    async def start(self):
        self.logger.debug(f'endpoint {self.id} started')
        self.running=True
        while self.running==True:
            await asyncio.sleep(self.delay)

    def send(message):
        return NotImplementedError

    def json_format():
        return NotImplementedError

    
