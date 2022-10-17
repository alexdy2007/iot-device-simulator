from endpoints.endpoint import EndPoint
from typing import List


class EndPointStore():

    def __init__(self, initial_endpoints:List[EndPoint]=None):
        
        if initial_endpoints==None:
            self.endpoints = []
        else:
            self.endpoints = initial_endpoints

    def add_endpoint(self, endpoint:EndPoint):
        self.endpoints.append(endpoint)

    def get_all_endpoints(self):
        return self.endpoints

    def get_endpoint_by_id(self, id):
        return [x for x in self.endpoints if x.id==id][0]