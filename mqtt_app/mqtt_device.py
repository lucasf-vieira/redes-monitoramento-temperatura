from modules.device_connection import DeviceConnection
import socket
import paho.mqtt.client as mqtt


class MQTTDevice(DeviceConnection):
    def __init__(self, device_ip, mqtt_broker_ip, mqtt_port = 1883, device_topic = "topico generico"):
        self.device_ip = device_ip
        self.mqtt_broker_ip = mqtt_broker_ip
        self.mqtt_port = mqtt_port
        self.device_topic = device_topic
        
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.connect(self.mqtt_broker_ip, self.mqtt_port)
        self.initialize()

    def close(self):
        self.close_connection()
        self.mqtt_client.disconnect()

    def _send_to_device(self, mensagem):
        topico = f"{self.device_topic}/{self.device_ip}"
        self.mqtt_client.publish(topico, mensagem)

    def _read_from_device(self):
        pass
    def on_mqtt_connect(self, cleint, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao Broker MQTT")
            topico = f"{self.device_topic}/{self.device_ip}"
            self.mqtt_client.subscribe(topico)
        else:
            print("Falha ao conectar-se ao Broker")
