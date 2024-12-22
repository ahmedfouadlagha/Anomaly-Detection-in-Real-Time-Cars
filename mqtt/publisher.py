# mqtt/publisher.py

import time
import random
import json
import paho.mqtt.client as mqtt
from config import BROKER, PORT, TOPIC

# Simulated car IDs
car_ids = [f"car_{i}" for i in range(1, 11)]

# Function to generate random car data
def generate_car_data(car_id):
    return {
        "car_id": car_id,
        "speed": random.randint(40, 120),  # Speed in km/h
        "engine_temp": random.uniform(70, 100),  # Engine temperature in °C
        "gps_lat": round(random.uniform(-90, 90), 6),  # Latitude
        "gps_long": round(random.uniform(-180, 180), 6),  # Longitude
        "timestamp": int(time.time())  # Current timestamp
    }

# MQTT connection
def connect_mqtt():
    client = mqtt.Client()
    client.connect(BROKER, PORT)
    return client

# Publish messages to the broker
def publish_data(client):
    while True:
        for car_id in car_ids:
            data = generate_car_data(car_id)
            client.publish(TOPIC, json.dumps(data))
            print(f"Published: {data}")
        time.sleep(1)  # Publish every second

if __name__ == "__main__":
    mqtt_client = connect_mqtt()
    try:
        publish_data(mqtt_client)
    except KeyboardInterrupt:
        print("Simulation stopped.")
        mqtt_client.disconnect()
