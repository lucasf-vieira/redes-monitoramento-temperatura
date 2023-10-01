import socket
from client import Client


class SocketClient(Client):
    CLIENT_IP = "127.0.0.1"
    CLIENT_PORT = 47107

    def __init__(self):
        super().__init__()
        self.running = True
        self.configure_sockets()

    def configure_sockets(self):
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        # print(f"Server IP {client_address} connected")

        data = connection_socket.recv(1024).decode("utf8")
        if data != "":
            print(f"Got {data} from {client_address}")

        connection_socket.close()
        return data


if __name__ == "__main__":
    client = SocketClient()
    client.setup("127.0.0.1", 47108)  # Configure o IP e a porta do servidor
    client.run()
