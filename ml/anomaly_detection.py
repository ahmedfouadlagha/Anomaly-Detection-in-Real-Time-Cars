# ml/anomaly_detection.py

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# File paths
PROCESSED_DATA_FILE = "data/processed/processed_data.csv"
MODEL_SAVE_PATH = "ml/models/anomaly_detector.h5"

# Load and preprocess the data
def load_and_preprocess_data():
    print("Loading processed data...")
    df = pd.read_csv(PROCESSED_DATA_FILE)

    # Select features for anomaly detection
    features = ["speed", "engine_temp", "speed_diff", "temp_normalized"]
    X = df[features].values

    # Standardize features
    print("Standardizing features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)

    return X_train, X_test, scaler

# Build the anomaly detection model (Autoencoder)
def build_model(input_dim):
    print("Building anomaly detection model...")
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(input_dim,)),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(input_dim, activation="linear"),  # Reconstruct the input
    ])
    model.compile(optimizer="adam", loss="mse")
    return model

# Train the model
def train_model(model, X_train):
    print("Training model...")
    history = model.fit(
        X_train,
        X_train,  # Autoencoders use input data as the target
        epochs=50,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )
    return history

# Evaluate the model and detect anomalies
def detect_anomalies(model, X_test):
    print("Evaluating model and detecting anomalies...")
    # Compute reconstruction error
    reconstructions = model.predict(X_test)
    reconstruction_errors = np.mean((X_test - reconstructions) ** 2, axis=1)

    # Set threshold as mean + 3 * std deviation of reconstruction errors
    threshold = np.mean(reconstruction_errors) + 3 * np.std(reconstruction_errors)
    anomalies = reconstruction_errors > threshold

    print(f"Anomaly detection threshold: {threshold}")
    print(f"Number of anomalies detected: {np.sum(anomalies)}")

    return reconstruction_errors, threshold, anomalies

if __name__ == "__main__":
    # Load and preprocess data
    X_train, X_test, scaler = load_and_preprocess_data()

    # Build the model
    model = build_model(input_dim=X_train.shape[1])

    # Train the model
    train_model(model, X_train)

    # Save the trained model
    print(f"Saving model to {MODEL_SAVE_PATH}...")
    model.save(MODEL_SAVE_PATH)

    # Detect anomalies
    detect_anomalies(model, X_test)

    print("Anomaly detection complete.")
