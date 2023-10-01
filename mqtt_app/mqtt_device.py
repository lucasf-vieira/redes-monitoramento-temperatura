from modules.device_connection import DeviceConnection
from mqtt_app.mqtt_constants import MQTT_BROKER_HOST, MQTT_BROKER_PORT
import paho.mqtt.client as mqtt


class MQTTDevice(DeviceConnection):
    def __init__(self, device_id):
        self.device_id = device_id
        self.data_from_device = None
        
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
        self.mqtt_client.loop_start()
        self.initialize()

    def on_message(self, client, userdata, msg):
        temperatura = float(msg.payload.decode())
        self.data_from_device = temperatura

    def on_mqtt_connect(self, client, userdata, flags, rc):
        topico = f"{self.device_id}_temperature"
        self.mqtt_client.subscribe(topico)

    def close(self):
        self.close_connection()
        self.mqtt_client.disconnect()

    def _send_to_device(self, mensagem):
        topico = f"{self.device_id}_command"
        self.mqtt_client.publish(topico, mensagem)

    def _read_from_device(self):
        if self.data_from_device:
            data = self.data_from_device
            self.data_from_device = None
            return data
