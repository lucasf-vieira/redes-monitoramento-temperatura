import time
from .mqtt_constants import MQTT_BROKER_HOST, MQTT_TOPIC
import paho.mqtt.client as mqtt
from temperature_read import Temperature


def on_publish(client, userdata, mid):
    print(f"Message published. #{mid}")


temp_reader = Temperature()
mqtt_client = mqtt.Client()
mqtt_client.on_publish = on_publish
mqtt_client.connect(MQTT_BROKER_HOST, 1883)  # Conecte-se a um servidor MQTT


if __name__ == "__main__":
    mqtt_client.loop_start()

    try:
        print("MQTT publisher started.")
        while True:
            mqtt_client.publish(MQTT_TOPIC, temp_reader.read_temperature())
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()
        print("MQTT publisher closed.")
