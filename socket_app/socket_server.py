import socket
from http_app.http_request import HttpRequest
from http_app.http_constants import JsonFormat
from .socket_client import SocketClient
import json
import time


socket_tcp = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
socket_udp = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

socket_tcp.bind(("::", 1028))  # Porta para conexão TCP
socket_udp.bind(("::", 1028))  # Porta para conexão UDP


try:
    # print("Iniciando servidor UDP e TCP")
    while True:
        # socket_tcp.connect(("127.0.0.1", 1027))
        # data = {"command": "set_x", "value": 2}
        # data = json.dumps(data)
        # tcp_conn.sendto(data.encode(), ("127.0.0.1", 1027))
        # data = tcp_conn.recv(1024)
        # temperature = int(data.decode("utf-8"))
        # print(f"Temperatura lida: {temperature}")
        # time.sleep(4)

        data, device_address = socket_udp.recvfrom(1024)
        temperature = float(data.decode("utf-8"))
        print(f"------------------------------------------")
        print(f"Lista de dispositivos:")
        print(f"'{device_address}' {temperature}")
except KeyboardInterrupt:
    socket_tcp.close()
    # tcp_conn.close()
