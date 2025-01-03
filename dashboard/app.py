from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import threading
import json
import paho.mqtt.client as mqtt
import os
import logging

# MQTT Configuration
BROKER_ADDRESS = os.getenv('BROKER_ADDRESS', "broker.hivemq.com")
DATA_TOPIC = os.getenv('DATA_TOPIC', "cars/data")
ANOMALY_TOPIC = os.getenv('ANOMALY_TOPIC', "cars/anomalies")
CLIENT_ID = os.getenv('CLIENT_ID', "DashboardService")

# Flask App Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
socketio = SocketIO(app)

# Global variables to store incoming data
car_data_store = []
anomaly_data_store = []

# Set up logging
logging.basicConfig(level=logging.INFO)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe([(DATA_TOPIC, 0), (ANOMALY_TOPIC, 0)])
    logging.info(f"Subscribed to topics: {DATA_TOPIC}, {ANOMALY_TOPIC}")

def on_message(client, userdata, msg):
    try:
        message = json.loads(msg.payload.decode())
        topic = msg.topic

        if topic == DATA_TOPIC:
            if len(car_data_store) > 100:  # Limit the size
                car_data_store.pop(0)
            car_data_store.append(message)
            socketio.emit('car_data', message)

        elif topic == ANOMALY_TOPIC:
            if len(anomaly_data_store) > 100:  # Limit the size
                anomaly_data_store.pop(0)
            anomaly_data_store.append(message)
            socketio.emit('anomaly_data', message)
        
        logging.info(f"Received on {topic}: {message}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

# Start MQTT Client
def mqtt_thread():
    client = mqtt.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(BROKER_ADDRESS, 1883, 60)
        client.loop_forever()
    except Exception as e:
        logging.error(f"MQTT connection error: {e}")

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({"car_data": car_data_store, "anomalies": anomaly_data_store})

@socketio.on('disconnect')
def handle_disconnect():
    logging.info("Client disconnected")

if __name__ == "__main__":
    # Start MQTT in a separate thread
    mqtt_thread_instance = threading.Thread(target=mqtt_thread)
    mqtt_thread_instance.start()
    # Run Flask app
    socketio.run(app, debug=True)

    # Ensure MQTT client is stopped on shutdown
    mqtt_thread_instance.join()