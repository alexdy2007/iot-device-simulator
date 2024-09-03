from typing import List
import logging
import asyncio
from device_simulator.device import Device
import sys
import threading
from queue import Queue

class DeviceRunner(threading.Thread):

    def __init__(self, device_list:List[Device]):

        super().__init__()

        self.setDaemon(True)
        self.logger = self.create_logger()
        self._devices = {d.device_id:{'task': None, 'device':d} for d in device_list}
        self.loop = asyncio.new_event_loop()
        self.start()

    @staticmethod
    def create_logger():
        h1 = logging.StreamHandler(sys.stdout)
        if __debug__:
            h1.setLevel(logging.DEBUG)
        else:
            h1.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        h1.setFormatter(formatter)
        logger = logging.getLogger('DeviceRunner')
        return logger

    def add_device(self, device):
        self._devices[device.device_id] = {'task': None, 'device':device}
        self.start_device(device.device_id)

    def is_device_running(self, device_id):
        try:
            device_item = self.get_device_item(device_id)
        except KeyError:
            return False

        return device_item['task']!=None

    def get_device(self, device_id):
        device = self._devices.get(device_id, {}).get('device', None)
        if device == None:
            self.logger.error(f'Device not found with id {device_id}')
            raise KeyError(f'Device not found with id {device_id}')
        return device

    def get_all_devices(self):
        return [d['device'] for d in self._devices.values()]

    def get_device_item(self, device_id):
        device_item = self._devices.get(device_id, None)
        if device_item == None:
            self.logger.error(f'Device not found with id {device_id}')
            raise KeyError(f'Device not found with id {device_id}')
        return device_item

    def get_last_n_readings_from_all_devices(self, n=10):
        device_results = {}
        for device_id, device_item in self._devices.items():
            device_results[device_id] = device_item.get('device').get_last_n_readings(n)
        return device_results

    def get_last_n_readings_from_device(self, device_id, n=10):
        try:
            device = self.get_device(device_id)
        except KeyError as e:
            raise e
        return device.get_last_n_readings(n)

    def get_number_running_devices(self):
        device_count_running = 0
        for d in self._devices.values():
            if d['device'].running==True:
                device_count_running += 1
        return device_count_running
    
    def get_number_stoped_devices(self):
        device_count_stopped= 0
        for d in self._devices.values():
            if d['device'].running==False:
                device_count_stopped += 1
        return device_count_stopped


    def remove_device(self, device_id):
        self.logger.debug(f'Removing device: {device_id}')
        self.stop_device(device_id)
        device_obj = self._devices.pop(device_id)
        del device_obj

    def remove_all_devices(self):
        self.logger.debug(f'Removing all devices')

        for device_id in self._devices.keys():
            self.remove_device(device_id)
        self._devices = {}
        return True

    def run(self):
        
        self.logger.debug('Starting device runner')

        asyncio.set_event_loop(self.loop)

        if __debug__:
            self.loop.set_debug(True)

        try:
            self.loop.run_forever()
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()        

    def start_all_devices(self):
        self.logger.debug(f'Starting All devices')
        for device_id in self._devices.keys():
            self.start_device(device_id)


    def start_device(self, device_id):
        
        if self.is_device_running(device_id)==True:
            self.logger.warning('device: {device_id} already running')
            return False

        try:
            device = self.get_device(device_id)
        except KeyError:
            return False
        future = asyncio.run_coroutine_threadsafe(device.start(), self.loop)
        self._devices[device.device_id]['task'] = future 
        self.logger.info(f'Starting Device with ID {device.device_id}')
        return True


    def stop_all_devices(self):
        self.logger.debug(f'Stopping All devices')

        for device_id in self._devices.keys():
            self.stop_device(device_id)


    def stop_device(self, device_id):
        
        if self.is_device_running(device_id)==False:
            self.logger.debug(f'Device {device_id} already stoped, cant stop')
            return False

        try:
            device_task = self.get_device_item(device_id)
            self.logger.info(f'Stopping Device with ID {device_id}')
            self._devices[device_id]['device'].stop()
            self.loop.call_soon_threadsafe(device_task['task'].cancel)
            self._devices[device_id]['task'] = None
        except KeyError:
            pass
     
        return True

    def stop_runner(self):
        self.stop_all_devices()
        if self.loop.is_running == True:
            self.loop.call_soon_threadsafe(self.loop.stop)