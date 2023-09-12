SERVER_URL = "http://127.0.0.1:5000"


class JsonFormat:
    def __init__(self, protocol, data):
        self.json_string = '{'+f'"{protocol}": '+f'"{data}"'+'}'
