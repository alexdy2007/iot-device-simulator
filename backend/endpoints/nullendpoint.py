from endpoints.endpoint import EndPoint

class NullEndpointConfig(EndPoint):

    def __init__(self) -> None:
        super().__init__(name='None')
        self.id=-1

    def send(message):
        return NotImplementedError

    def json_format(self):
        return {
            "name":self.name,
            "id": self.id
        }
