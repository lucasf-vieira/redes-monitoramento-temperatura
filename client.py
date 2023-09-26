import time
from modules.temperature import Temperature
from modules.timer import TimerSeconds
from enum import Enum
import json


class Commands(Enum):
    SET_X = "set_x"
    SET_Y = "set_y"
    RESET = "reset"
    SETUP = "setup"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Client:
    def __init__(self):
        self.server_ip = None
        self.server_port = None
        self.readings = []
        self.x_interval = 2  # Valor padrão de X
        self.y_interval = 1  # Valor padrão de Y

    def setup(self, server_ip, server_port):
        self.server_ip = str(server_ip)
        self.server_port = int(server_port)

    def reset(self):
        self.readings = []

    def set_x(self, x):
        self.x_interval = int(x)

    def set_y(self, y):
        self.y_interval = int(y)

    def read_temperature(self):
        temperature = Temperature().read_temperature()
        self.readings.append(temperature)

    def send_average_temperature(self):
        if not self.server_ip or not self.server_port:
            print("IP e porta do servidor não configurados.")
            return

        if len(self.readings) == 0:
            print("Nenhuma leitura para enviar a média.")
            return

        average_temperature = sum(self.readings) / len(self.readings)
        self._send(average_temperature)

    def read_command(self):
        command_string = self._read()
        # Checar se o commando é valido
        if command_string == "":
            return
        print(f"data read: {command_string}")
        try:
            command_json = json.loads(command_string)
        except Exception:
            return
        if not isinstance(command_json, dict):
            return
        if not Commands.has_value(command_json["command"]):
            return
        command_method = getattr(self, command_json["command"])
        if command_json["command"] == Commands.SETUP.value:
            command_method(
                command_json["value"]["server_ip"],
                command_json["value"]["server_port"]
            )
        command_method(command_json["value"])

    def _read(self) -> str:
        """
        This method MUST be implemented in child class.
        """
        raise NotImplementedError()

    def _send(self, average_temperature) -> None:
        """
        This method MUST be implemented in child class.
        """
        raise NotImplementedError()

    def run(self):
        x_timer = TimerSeconds()
        y_timer = TimerSeconds()
        while True:
            self.read_command()
            if y_timer.elapsed_time() >= self.y_interval:
                y_timer.reset()
                self.read_temperature()

            if x_timer.elapsed_time() >= self.x_interval:
                x_timer.reset()
                self.send_average_temperature()

            time.sleep(0.05)


if __name__ == "__main__":
    client = Client()
    client.setup("127.0.0.1", 8080)  # Configure o IP e a porta do servidor
    client.run()
