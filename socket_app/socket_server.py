import socket
from http_app.http_request import HttpRequest
from http_app.http_constants import JsonFormat
from .socket_client import SocketClient
import json
import time


# Configuração Socket TCP
# tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# tcp_server.bind(("0.0.0.0", 1025))  # Porta para conexão TCP
# tcp_server.listen(5)

socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket_tcp.bind(("0.0.0.0", 1028))  # Porta para conexão TCP
socket_udp.bind(("0.0.0.0", 1028))  # Porta para conexão TCP

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

        data = socket_udp.recv(1024)
        temperature = float(data.decode("utf-8"))
        print(f"Temperatura lida: {temperature}")
except KeyboardInterrupt:
    socket_tcp.close()
    # tcp_conn.close()
