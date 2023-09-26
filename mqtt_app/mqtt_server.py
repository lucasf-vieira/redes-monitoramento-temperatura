import time
import paho.mqtt.client as mqtt
from .mqtt_constants import MQTT_BROKER_HOST, MQTT_TOPIC
from http_app.http_request import HttpRequest
from http_app.http_constants import JsonFormat


if __name__ == "__main__":
    # Callback function to handle incoming messages
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        print(f"Received message: {message}")
        HttpRequest().update_temperature(JsonFormat("mqtt", message))

    # Create an MQTT client
    mqtt_client = mqtt.Client()

    # Set the message callback function
    mqtt_client.on_message = on_message

    # Connect to the MQTT broker
    mqtt_client.connect(MQTT_BROKER_HOST, 1883)
    mqtt_client.subscribe(MQTT_TOPIC)
    mqtt_client.loop_start()
    print("MQTT subscriber started.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()
        print("MQTT publisher closed.")
