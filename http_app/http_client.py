from client import Client
from flask import Flask, request
import threading as th
import requests


class HTTPClient(Client):
    def __init__(self):
        super().__init__()
        self._device_command = None
        self._device_temperature = self._temperature
        self.flask_server = Flask(__name__)

        self.flask_thread = th.Thread(target=self.run_flask)
        self.flask_thread.start()

        @self.flask_server.route("/command", methods=["POST"])
        def command():
            command = request.get_data()
            self._device_command = command
            return "Command received successfully"

    def run_flask(self):
        self.flask_server.run(host="0.0.0.0", port=5000)

    def _read(self) -> str:
        if self._device_command is not None:
            command = self._device_command
            self._device_command = None
            return command

    def _send(self, average_temperature):
        try:
            response = requests.post(f"http://{self.server_ip}:{self.server_port}/temperature", data=str(average_temperature).encode())
        except:
            return
        if response.status_code != 200:
            print(f"Failed to send temperature. Status code: {response.status_code}")


if __name__ == "__main__":
    client = HTTPClient()
    client.setup("127.0.0.1", 5001)  # Configure o IP e a porta do servidor
    client.run()
