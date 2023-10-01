from modules.device_connection import DeviceConnection
import socket


class SocketDevice(DeviceConnection):
    def __init__(self, device_ip):
        self.device_id = device_ip

        self._socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket_udp.bind(("0.0.0.0", self.SERVER_PORT))

        self.initialize()

    def close(self):
        self.close_connection()

        self._socket_tcp.close()
        self._socket_udp.close()

    def tcp_connect(self):
        self._socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket_tcp.connect((self.device_id, self.DEVICE_PORT))

    def _send_to_device(self, data: str):
        self.tcp_connect()
        data = data.encode()
        self._socket_tcp.sendto(data, (self.device_id, self.DEVICE_PORT))
        self._socket_tcp.close()

    def _read_from_device(self):
        data = self._socket_udp.recv(1024)
        return data.decode()
