# mqtt/car_data_simulator.py

import json
import random
import time
import paho.mqtt.client as mqtt

# MQTT Configuration
BROKER_ADDRESS = "broker.hivemq.com"
PUBLISH_TOPIC = "cars/data"
CLIENT_ID = "CarDataSimulator"

# Simulate car telemetry data
CAR_IDS = [f"car_{i:02d}" for i in range(1, 11)]

def generate_car_data(car_id):
    """Generate random telemetry data for a car."""
    speed = random.uniform(60, 120)  # Speed in km/h
    engine_temp = random.uniform(80, 120)  # Engine temperature in °C
    speed_diff = random.uniform(-0.5, 0.5)  # Change in speed
    temp_normalized = (engine_temp - 80) / 40  # Normalized temperature (0-1)

    return {
        "car_id": car_id,
        "speed": round(speed, 2),
        "engine_temp": round(engine_temp, 2),
        "speed_diff": round(speed_diff, 2),
        "temp_normalized": round(temp_normalized, 2),
    }

# MQTT publishing function
def publish_data(client):
    try:
        while True:
            for car_id in CAR_IDS:
                car_data = generate_car_data(car_id)
                payload = json.dumps(car_data)
                client.publish(PUBLISH_TOPIC, payload)
                print(f"Published: {payload}")
                time.sleep(1)  # Simulate a delay between messages
    except KeyboardInterrupt:
        print("Simulation stopped.")

# Initialize MQTT client
def start_simulation():
    print("Starting car data simulation...")
    client = mqtt.Client(CLIENT_ID)
    client.connect(BROKER_ADDRESS, 1883, 60)

    try:
        publish_data(client)
    finally:
        print("Disconnecting MQTT client...")
        client.disconnect()

if __name__ == "__main__":
    start_simulation()
