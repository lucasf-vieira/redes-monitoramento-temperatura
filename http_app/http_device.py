from modules.device_connection import DeviceConnection
import requests
from flask import Flask, request
import multiprocessing as mp
import logging



def run_flask(queue: mp.Queue):
    flask_server = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.CRITICAL)

    @flask_server.route("/temperature", methods=['POST'])
    def temperature():
        temperature = request.get_data()
        queue.put(temperature)
        return "Temperature received successfully"

    flask_server.run(host="0.0.0.0", port=5001)


class HTTPDevice(DeviceConnection):
    def __init__(self, device_id, http_port=5000):
        self.device_id = device_id
        self.device_url = f"http://{device_id}:{http_port}"

        self.temperature_queue = mp.Queue()
        self.flask_process = mp.Process(target=run_flask, args=(self.temperature_queue,))
        self.flask_process.start()
        self.initialize()

    def close(self):
        self.close_connection()
        self.flask_process.terminate()

    def _send_to_device(self, data):
        response = requests.post(f"{self.device_url}/command", data=data)
        if response.status_code != 200:
            print(f"Failed to send data to device. Status code: {response.status_code}")

    def _read_from_device(self):
        temperature: bytes = self.temperature_queue.get(block=True)
        return temperature.decode()
