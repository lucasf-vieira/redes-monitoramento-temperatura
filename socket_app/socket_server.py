import socket
from http_app.http_request import HttpRequest
from http_app.http_constants import JsonFormat
import json
import time


# Configuração Socket TCP
# tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# tcp_server.bind(("0.0.0.0", 1025))  # Porta para conexão TCP
# tcp_server.listen(5)

socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_tcp.bind(("0.0.0.0", 1028))  # Porta para conexão UDP
# socket_tcp.connect(("127.0.0.1", 1027))
socket_tcp.listen(5)
# tcp_server.listen(5)


try:
    print("Iniciando servidor UDP e TCP")
    tcp_conn, addr = socket_tcp.accept()
    while True:
        # tcp_conn, addr = tcp_server.accept()
        # print("Conectado em", addr)
        # data_tcp = tcp_conn.recv(1024)
        # print("Mensagem TCP recebida: ", str(data_tcp))

        # data_tcp = data_tcp.decode()
        # HttpRequest().update_temperature(JsonFormat("tcp", data_tcp))
        print("Conectado em", addr)
        # tcp_conn.recv
        data = {"command": "set_x", "value": 2}
        data = json.dumps(data)
        tcp_conn.sendto(data.encode(), ("127.0.0.1", 1027))
        time.sleep(4)
        # print("Conectado em", addr)
        # print("Mensagem UDP recebida: ", str(data_udp))

        # data_udp = data_udp.decode()
        # HttpRequest().update_temperature(JsonFormat("udp", data_udp))
except KeyboardInterrupt:
    socket_tcp.close()
    # tcp_conn.close()
