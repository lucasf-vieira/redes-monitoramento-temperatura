import socket
from client import Client
from modules.timer import TimerSeconds
import threading as th
import time


class SocketClient(Client):
    CLIENT_IP = "0.0.0.0"
    CLIENT_PORT = 1027

    def __init__(self):
        super().__init__()
        self.running = True
        self.configure_sockets()

    def configure_sockets(self):
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.temperature_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.command_socket.bind((self.CLIENT_IP, self.CLIENT_PORT))
        self.temperature_socket.bind((self.CLIENT_IP, self.CLIENT_PORT))

        self.command_socket.listen()
        print("Sockets configured")

    def _send(self, average_temperature):
        print(f"Sending temperature to {self.server_ip}:{self.server_port}")
        self.temperature_socket.sendto(
            bytes(str(average_temperature), "utf8"), (self.server_ip, self.server_port)
        )

    def _read(self):
        connection_socket, client_address = self.command_socket.accept()
        print(f"Server IP {client_address} connected")

        data = connection_socket.recv(1024).decode("utf8")
        print(f"Got {data} from {client_address}")

        connection_socket.close()
        return data

    def _commands_receiver(self):
        while self.running:
            self.read_command()

    def run(self):
        x_timer = TimerSeconds()
        y_timer = TimerSeconds()

        commands_thread = th.Thread(target=self._commands_receiver)
        commands_thread.daemon = True
        commands_thread.start()
        while True:
            if y_timer.elapsed_time() >= self.y_interval:
                self.read_temperature()
                y_timer.reset()

            if x_timer.elapsed_time() >= self.x_interval:
                self.send_average_temperature()
                x_timer.reset()

            time.sleep(0.05)


if __name__ == "__main__":
    client = SocketClient()
    client.setup("127.0.0.1", 1028)  # Configure o IP e a porta do servidor
    client.run()
