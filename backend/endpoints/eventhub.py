from endpoints.endpoint import EndPoint

class EventhubConfig(EndPoint):

    def __init__(self, name:str, connection_string:str) -> None:
        self.connection_string = connection_string
        super().__init__(name)

    def send(message):
        return NotImplementedError

    def json_format(self):
        return {
            "name":self.name,
            "connection_string":self.connection_string,
            "id": self.id
        }

