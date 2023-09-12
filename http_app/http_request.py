import requests
import traceback as tb
from .http_constants import SERVER_URL, JsonFormat
import json


class HttpRequest:
    def post(self, server_route: str, data: JsonFormat):
        if not isinstance(data, JsonFormat):
            raise ValueError("Data format expected: JsonFormat")
        try:
            data_to_send = json.loads(data.json_string)
            response = requests.post(SERVER_URL + "/" + server_route, json=data_to_send)
            if response.status_code != 200:
                print(f"Failed to send data. Status code: {response.status_code}")
        except Exception:
            tb.print_exc()

    def update_temperature(self, data: JsonFormat):
        self.post("update_data", data)
