from device_simulator.distributions import NormalDist, BetaDist
from device_simulator.device import Device

def create_dummy_device(delay=10, location="Eccup Resevouir"):

    attributes = {
            "Voltage":NormalDist(10,1),
            "Amp":BetaDist(1,1,10)
        }

    meta_data = {
        "Location":location
    }

    device = Device(delay=delay, attributes=attributes, meta_data=meta_data)


    return device