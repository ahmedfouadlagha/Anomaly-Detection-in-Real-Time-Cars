# visualization/visualize_anomalies.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# File paths
PROCESSED_DATA_FILE = "data/processed/processed_data.csv"
MODEL_SAVE_PATH = "ml/models/anomaly_detector.h5"

def visualize_anomalies():
    if not os.path.exists(PROCESSED_DATA_FILE):
        print(f"Processed data file not found: {PROCESSED_DATA_FILE}")
        return

    if not os.path.exists(MODEL_SAVE_PATH):
        print(f"Model file not found: {MODEL_SAVE_PATH}")
        return

    try:
        # Load the processed data
        print("Loading processed data...")
        df = pd.read_csv(PROCESSED_DATA_FILE)

        # Select features and standardize
        features = ["speed", "engine_temp", "speed_diff", "temp_normalized"]
        X = df[features].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Load the trained model
        print("Loading trained model...")
        model = load_model(MODEL_SAVE_PATH)

        # Predict reconstruction errors
        print("Predicting reconstruction errors...")
        reconstructions = model.predict(X_scaled)
        reconstruction_errors = np.mean((X_scaled - reconstructions) ** 2, axis=1)

        # Set anomaly detection threshold
        threshold = np.mean(reconstruction_errors) + 3 * np.std(reconstruction_errors)

        # Identify anomalies
        anomalies = reconstruction_errors > threshold
        df["Reconstruction Error"] = reconstruction_errors
        df["Anomaly"] = anomalies

        # Save results
        anomaly_output_path = "data/results/anomalies.csv"
        os.makedirs(os.path.dirname(anomaly_output_path), exist_ok=True)
        df.to_csv(anomaly_output_path, index=False)
        print(f"Anomaly results saved to: {anomaly_output_path}")

        # Plot reconstruction errors
        print("Plotting reconstruction errors...")
        plt.figure(figsize=(10, 6))
        plt.plot(reconstruction_errors, label="Reconstruction Error")
        plt.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold ({threshold:.4f})")
        plt.scatter(
            np.where(anomalies)[0], 
            reconstruction_errors[anomalies], 
            color="red", 
            label="Anomalies"
        )
        plt.title("Reconstruction Errors with Detected Anomalies")
        plt.xlabel("Sample Index")
        plt.ylabel("Reconstruction Error")
        plt.legend()
        plt.savefig("visualization/reconstruction_errors_with_anomalies.png")  # Save plot
        plt.show()

        print("Visualization complete. Check 'visualization/' directory for the plot.")

    except Exception as e:
        print(f"Error during anomaly visualization: {e}")

if __name__ == "__main__":
    visualize_anomalies()
