import socket
from http_app.http_request import HttpRequest
from http_app.http_constants import JsonFormat


# Configuração Socket TCP
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind(("0.0.0.0", 1025))  # Porta para conexão TCP
tcp_server.listen(5)

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(("0.0.0.0", 1027))  # Porta para conexão UDP

try:
    print("Iniciando servidor UDP e TCP")
    while True:
        tcp_conn, addr = tcp_server.accept()
        print("Conectado em", addr)
        data_tcp = tcp_conn.recv(1024)
        print("Mensagem TCP recebida: ", str(data_tcp))
        # tcp_conn.sendall(data_tcp)

        data_tcp = data_tcp.decode()
        HttpRequest().update_temperature(JsonFormat("tcp", data_tcp))

        data_udp, addr = udp_server.recvfrom(1024)
        print("Conectado em", addr)
        print("Mensagem UDP recebida: ", str(data_udp))

        data_udp = data_udp.decode()
        HttpRequest().update_temperature(JsonFormat("udp", data_udp))

        # resposta = "Echo=>" + str(data_udp)
        # udp_server.sendto(data_udp, addr)
except KeyboardInterrupt:
    udp_server.close()
    tcp_conn.close()
