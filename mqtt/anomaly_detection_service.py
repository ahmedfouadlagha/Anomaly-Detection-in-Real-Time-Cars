# mqtt/anomaly_detection_service.py

import json
import numpy as np
import pandas as pd
import paho.mqtt.client as mqtt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# MQTT Configuration
BROKER_ADDRESS = "broker.hivemq.com"
SUBSCRIBE_TOPIC = "cars/data"
PUBLISH_TOPIC = "cars/anomalies"
CLIENT_ID = "AnomalyDetectionService"

# File paths
MODEL_PATH = "ml/models/anomaly_detector.h5"
SCALER_PATH = "ml/models/scaler.pkl"

# Load the trained model and scaler
print("Loading model and scaler...")
model = load_model(MODEL_PATH)
scaler = StandardScaler()  # Assume scaler is initialized manually for simplicity

# Define MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(SUBSCRIBE_TOPIC)
    print(f"Subscribed to topic: {SUBSCRIBE_TOPIC}")

def on_message(client, userdata, msg):
    try:
        print(f"Received message from topic {msg.topic}: {msg.payload.decode()}")
        
        # Parse incoming JSON data
        car_data = json.loads(msg.payload.decode())
        
        # Convert to DataFrame for processing
        df = pd.DataFrame([car_data])

        # Select and preprocess features
        features = ["speed", "engine_temp", "speed_diff", "temp_normalized"]
        X = df[features].values
        X_scaled = scaler.transform(X)

        # Predict reconstruction errors
        reconstructions = model.predict(X_scaled)
        reconstruction_errors = np.mean((X_scaled - reconstructions) ** 2, axis=1)

        # Set anomaly threshold
        threshold = 0.05  # Adjust based on training results
        is_anomaly = reconstruction_errors[0] > threshold

        # Publish result
        result = {
            "car_id": car_data["car_id"],
            "anomaly": is_anomaly,
            "reconstruction_error": reconstruction_errors[0],
        }
        client.publish(PUBLISH_TOPIC, json.dumps(result))
        print(f"Published anomaly result: {result}")

    except Exception as e:
        print(f"Error processing message: {e}")

# Initialize MQTT client
print("Initializing MQTT client...")
client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

# Start MQTT client
def start_mqtt_client():
    try:
        client.connect(BROKER_ADDRESS, 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("Disconnecting MQTT client...")
        client.disconnect()

if __name__ == "__main__":
    start_mqtt_client()
