import socket
from temperature_read import Temperature
import time


HOST = '127.0.0.1'
PORT_tcp = 1025
PORT_udp = 1027

instance = Temperature()

try:
    while True:
        temp_data = instance.read_temperature()
        temp_data = str(temp_data)

        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client.connect((HOST, PORT_tcp))
        except ConnectionRefusedError:
            continue
        tcp_client.sendall(str.encode(temp_data))

        time.sleep(0.2)
        temp_data = instance.read_temperature()
        temp_data = str(temp_data)

        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client.sendto(bytes(temp_data, "utf8"), (HOST, PORT_udp))

        print("Messages sent.")
        time.sleep(1)

        # data_udp, addr = udp_client.recvfrom(1024)

        # print("Mensagem UDP ecoada:", data_udp.decode())
except KeyboardInterrupt:
    pass
except Exception:
    import traceback as tb
    tb.print_exc()
