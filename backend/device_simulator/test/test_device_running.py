from device_simulator.device import Device
from device_simulator.distributions import BetaDist, NormalDist
from device_simulator.device_runner import DeviceRunner
from time import sleep
from datetime import datetime

attributes = {
        "Voltage":NormalDist(10,1),
        "Amp":BetaDist(1,1,10)
    }

meta_data = {
    "Location":"Eccup Resevouir"
}

def test_device_running_7_seconds():
   
    device_1 = Device(delay=1, attributes=attributes, meta_data=meta_data)

    device_to_run = [device_1]

    dr = DeviceRunner(device_to_run)
    
  
    dr.start_all_devices()
    sleep(7)

    results = dr.get_last_n_readings_from_device(device_1.device_id, 3)
    dr.stop_runner()

    assert len(results['Voltage'])>=3

def test_3_devices_running_7_seconds():

    device_1 = Device(delay=1, attributes=attributes, meta_data=meta_data)
    device_2 = Device(delay=3, attributes=attributes, meta_data=meta_data)
    device_3 = Device(delay=10, attributes=attributes, meta_data=meta_data)

    device_to_run = [device_1, device_2, device_3]

    dr = DeviceRunner(device_to_run)
    
  
    dr.start_all_devices()
    sleep(8)

    device_1_results = dr.get_last_n_readings_from_device(device_1.device_id, 3)
    device_2_results = dr.get_last_n_readings_from_device(device_2.device_id, 3)
    device_3_results = dr.get_last_n_readings_from_device(device_3.device_id, 3)

    dr.stop_runner()
    

    assert len(device_1_results['Voltage'])>=3, 'Results for device 1 should contain at least 3 readings'
    assert len(device_2_results['Voltage'])>=2, 'Results for device 2 should contain at least 2 readings'
    assert len(device_3_results['Voltage'])==1, 'Results for device 3 should contain 1 readings'

def test_add_2_devices_and_then_stop_one():

    device_1 = Device(delay=1, attributes=attributes, meta_data=meta_data)
    device_2 = Device(delay=3, attributes=attributes, meta_data=meta_data)

    device_to_run = [device_1, device_2]

    dr = DeviceRunner(device_to_run)
    
  
    dr.start_all_devices()
    sleep(8)

    dr.stop_device(device_1.device_id)
    sleep(1)
    running_dev = dr.get_number_running_devices()
    stopped_dev = dr.get_number_stoped_devices()

    dr.stop_runner()
    

    assert running_dev==1, 'Number of running devices is 1'
    assert stopped_dev==1, 'Number of stopped devices is 1'


def test_make_sure_device_stops():
    device_1 = Device(delay=1, attributes=attributes, meta_data=meta_data)

    device_to_run = [device_1]

    dr = DeviceRunner(device_to_run)
    
  
    dr.start_all_devices()
    sleep(6)

    dr.stop_device(device_1.device_id)
    sleep(10)

    stopped_dev = dr.get_number_stoped_devices()
    

    voltage_attr = device_1.attributes_history['Voltage']
    times = [x['time'] for x in voltage_attr]
    last_time = sorted(times, reverse=True)[0]
    time_diff = datetime.now() - last_time

    assert stopped_dev==1, 'make sure device has stopped'
    assert time_diff.seconds >= 10, "assert device stoped at least 10 seconds ago"

    dr.stop_runner()

def test_start_stop_start():
    
    device_1 = Device(delay=1, attributes=attributes, meta_data=meta_data)
    device_to_run = [device_1]
    dr = DeviceRunner(device_to_run)
    dr.start_all_devices()
    sleep(6)

    dr.stop_device(device_1.device_id)
    sleep(6)

    stoped_dev = dr.get_number_stoped_devices()
    restart_time = datetime.now()
    dr.start_device(device_1.device_id)
    sleep(6)

    started_dev = dr.get_number_running_devices()
    
    voltage_attr = device_1.attributes_history['Voltage']
    times = [x['time'] for x in voltage_attr]
    last_time = sorted(times, reverse=True)[0]
    time_diff = restart_time - last_time

    assert stoped_dev==1, 'make sure device was stopped'
    assert started_dev==1, 'make sure device was turned back on'
    assert time_diff.seconds > 0, "assert new reading occured after restart date"

    dr.stop_runner()

def test_add_new_device():
    
    device_1 = Device(delay=1, attributes=attributes, meta_data=meta_data)
    device_2 = Device(delay=1, attributes=attributes, meta_data=meta_data)

    device_to_run = [device_1]
    dr = DeviceRunner(device_to_run)
    dr.start_all_devices()

    sleep(6)
    dr.add_device(device_2)
    add_time = datetime.now()
    sleep(6)
    
    voltage_attr = device_2.attributes_history['Voltage']
    times = [x['time'] for x in voltage_attr]
    last_time = sorted(times, reverse=True)[0]
    time_diff = last_time - add_time

    num_running_devices = dr.get_number_running_devices()

    assert num_running_devices==2, 'make sure both devices running'
    assert time_diff.seconds > 0, "assert new reading occured after add date"

    dr.stop_runner()