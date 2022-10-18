from device_simulator.distributions import NormalDist, BetaDist
from device_simulator.device import Device
from queue import Queue

def create_dummy_device(delay=10, location="Eccup Resevouir", queue:Queue=None, endpoint_id=1):

    attributes = {
            "Voltage":NormalDist(10,1),
            "Amp":BetaDist(1,1,10)
        }

    meta_data = {
        "Location":location
    }

    device = Device(delay=delay, attributes=attributes, meta_data=meta_data, device_reading_queue=queue, endpoint_id=endpoint_id)


    return device