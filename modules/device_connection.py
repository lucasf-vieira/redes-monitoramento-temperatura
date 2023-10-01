import time
from constants.command import CommandEnum
import threading as th
import socket
import json


class DeviceConnection:
    DEVICE_PORT = 47107
    SERVER_PORT = 47108

    def __init__(self, device_id):
        self.device_id = device_id
        raise NotImplementedError()        

    def close(self):
        self.close_connection()
        raise NotImplementedError()

    def initialize(self):
        self.running = True
        self.temperature = ""
        self.command = None
        
        self.reader_thread = th.Thread(target=self._temperature_reader)
        self.sender_thread = th.Thread(target=self._command_sender)

        self.reader_thread.start()
        self.sender_thread.start()

    def close_connection(self):
        self.running = False
        self._close_threads()

    def get_temperature(self):
        return self.temperature

    def send_command(self, command, value):
        # Checar se o commando é valido
        if command == "":
            return False
        if not CommandEnum.has_value(command):
            return False
        data = {
            "command": command
        }
        if command == CommandEnum.SETUP.value:
            data.update({
                "value": {
                    "server_ip": value["server_ip"],
                    "server_port": value["server_port"]
                }
            })
        else:
            data.update({
                "value": value
            })
        self.command = data
        return True

    #
    #  Thread Methods
    #

    def _command_sender(self):
        while self.running:
            if self.command is not None:
                self._send_to_device(json.dumps(self.command))
                self.command = None
            time.sleep(0.05)

    def _temperature_reader(self):
        while self.running:
            temperature = self._read_from_device()
            if temperature is not None and temperature != "":
                self.temperature = float(temperature)
            time.sleep(0.05)

    #
    #  Private Methods
    #

    def _close_threads(self):
        self.reader_thread.join()
        self.sender_thread.join()

    def _send_to_device(self, data):
        raise NotImplementedError()

    def _read_from_device(self):
        raise NotImplementedError()

if __name__ == "__main__":
    device = DeviceConnection("127.0.0.1")
    device._command_sender(CommandEnum.RESET.value, "")
    device._command_sender(CommandEnum.SETUP.value, {"server_ip": "10.0.0.1", "server_port": 8880})
    device._command_sender(CommandEnum.SET_X.value, 10)
    