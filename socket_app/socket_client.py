import socket
from client import Client


class SocketClient(Client):
    CLIENT_IP = '0.0.0.0'
    CLIENT_PORT = 1027

    def __init__(self):
        super().__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind((self.CLIENT_IP, self.CLIENT_PORT))
        while True:
            try:
                self.client_socket.connect(("127.0.0.1", 1028))
                break
            except ConnectionRefusedError:
                continue
        self.client_socket.setblocking(False)

    def _send(self, average_temperature):
        self.client_socket.sendto(
            bytes(str(average_temperature), "utf8"),
            (self.server_ip, self.server_port)
        )

    def _read(self):
        try:
            data = self.client_socket.recv(1024)
        except BlockingIOError:
            return ""
        data = data.decode("utf8")
        print(f"data read: {data}")
        return data


if __name__ == "__main__":
    client = SocketClient()
    client.setup("127.0.0.1", 1027)  # Configure o IP e a porta do servidor
    client.run()
