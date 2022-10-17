class EndPoint():

    count = 0

    @classmethod
    def gen_id(cls):
        while True:
            cls.count = cls.count+1
            yield cls.count

    def __init__(self, name):
        self.id = next(self.gen_id())
        self.name = name

    def send(message):
        return NotImplementedError

    def json_format():
        return NotImplementedError

    
