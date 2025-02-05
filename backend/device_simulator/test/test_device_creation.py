from backend.device_simulator.device import Device
from backend.device_simulator.distributions import BetaDist, NormalDist

attributes = {
    "Voltage":NormalDist(10,1),
    "Amp":BetaDist(1,1,10)
}

meta_data = {
    "Location":"Eccup Resevouir"
}

def test_device_creation():

    device = Device(attributes=attributes, meta_data=meta_data)
    assert isinstance(device.attributes, dict)
    assert isinstance(device.meta_data, dict)
    assert isinstance(device.device_id, int)

def test_get_device_info():
    device = Device(attributes=attributes, meta_data=meta_data)
    device_info = device.get_device_info()

    assert device_info['delay']==10
    assert isinstance(device_info['device_id'], int)
    assert device_info['running']==False
    assert device_info['meta_data']['Location']=='Eccup Resevouir'
    assert device_info['attributes'][0]['name']=='Voltage'
    assert device_info['attributes'][0]['model']['dist_type']=='Normal'