# mqtt/subscriber.py

import json
import paho.mqtt.client as mqtt
from config import BROKER, PORT, TOPIC

# Callback when the client receives a message from the broker
def on_message(client, userdata, msg):
    try:
        # Decode and parse the message
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(f"Received: {data}")
        # Log the data to a file
        with open("mqtt/received_data.log", "a") as f:
            f.write(json.dumps(data) + "\n")
    except Exception as e:
        print(f"Error processing message: {e}")

# Callback when the client successfully connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

# Connect to the MQTT broker and start listening
def connect_and_subscribe():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_forever()

if __name__ == "__main__":
    try:
        connect_and_subscribe()
    except KeyboardInterrupt:
        print("Subscriber stopped.")
