from endpoints.endpoint import EndPoint
import asyncio

class NullEndpoint(EndPoint):

    def __init__(self) -> None:
        super().__init__(name='NullEndpointDefault')

    async def send(message):
        return True

    def json_format(self):
        return {
            "name":self.name,
            "id": self.id
        }

    async def start(self):        
        self.logger.debug(f'endpoint {self.name} with id:{self.id} started')
        self.running=True
        while self.running==True:
            self.messages_to_send = []
            await asyncio.sleep(10)
