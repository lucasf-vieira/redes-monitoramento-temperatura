# import time
# from .mqtt_constants import MQTT_BROKER_HOST, MQTT_TOPIC
# import paho.mqtt.client as mqtt
# from modules.temperature import Temperature


# def on_publish(client, userdata, mid):
#     print(f"Message published. #{mid}")


# temp_reader = Temperature()
# mqtt_client = mqtt.Client()
# mqtt_client.on_publish = on_publish
# mqtt_client.connect(MQTT_BROKER_HOST, 1883)  # Conecte-se a um servidor MQTT


# if __name__ == "__main__":
#     mqtt_client.loop_start()

#     try:
#         print("MQTT publisher started.")
#         while True:
#             mqtt_client.publish(MQTT_TOPIC, temp_reader.read_temperature())
#             time.sleep(1)
#     except KeyboardInterrupt:
#         mqtt_client.disconnect()
#         mqtt_client.loop_stop()
#         print("MQTT publisher closed.")

from .mqtt_constants import MQTT_BROKER_HOST, MQTT_BROKER_PORT
import paho.mqtt.client as mqtt
from client import Client
import time
import threading


class MQTTClient(Client):    
    def __init__(self, device_id):
        super().__init__()
        # Configuração MQTT
        self.device_id = device_id
        self.server_command = None
        self.MQTT_COMMAND_TOPIC = f"{device_id}_command"
        self.MQTT_TEMPERATURE_TOPIC = f"{device_id}_temperature"

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        self.mqtt_client.loop_start()

    # Funções MQTT
    def on_connect(self, client, userdata, flags, rc):
        print("Conectado ao servidor MQTT com código de resultado: " + str(rc))
        self.mqtt_client.subscribe(self.MQTT_COMMAND_TOPIC)

    def on_message(self, client, userdata, msg):
        command = msg.payload.decode()
        print("Comando recebido:", command)
        self.server_command = command

    def _read(self):
        if self.server_command:
            command = self.server_command
            self.server_command = None
            return command
    
    def _send(self, temperatura):
        print(f"Enviando temperatura para topico {self.MQTT_TEMPERATURE_TOPIC}")
        self.mqtt_client.publish(self.MQTT_TEMPERATURE_TOPIC, str(temperatura))

if __name__ == "__main__":
    client = MQTTClient("dispositivo_janela_quarto3")
    # client.setup("127.0.0.1", 47108)  # Configure o IP e a porta do servidor
    client.run()
