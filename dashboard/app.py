from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import threading
import json
import paho.mqtt.client as mqtt

# MQTT Configuration
BROKER_ADDRESS = "broker.hivemq.com"
DATA_TOPIC = "cars/data"
ANOMALY_TOPIC = "cars/anomalies"
CLIENT_ID = "DashboardService"

# Flask App Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Global variables to store incoming data
car_data_store = []
anomaly_data_store = []

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe([(DATA_TOPIC, 0), (ANOMALY_TOPIC, 0)])
    print(f"Subscribed to topics: {DATA_TOPIC}, {ANOMALY_TOPIC}")

def on_message(client, userdata, msg):
    try:
        message = json.loads(msg.payload.decode())
        topic = msg.topic

        if topic == DATA_TOPIC:
            car_data_store.append(message)
            socketio.emit('car_data', message)
        elif topic == ANOMALY_TOPIC:
            anomaly_data_store.append(message)
            socketio.emit('anomaly_data', message)
        
        print(f"Received on {topic}: {message}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Start MQTT Client
def mqtt_thread():
    client = mqtt.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_ADDRESS, 1883, 60)
    client.loop_forever()

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({"car_data": car_data_store, "anomalies": anomaly_data_store})

if __name__ == "__main__":
    # Start MQTT in a separate thread
    threading.Thread(target=mqtt_thread).start()
    # Run Flask app
    socketio.run(app, debug=True)
