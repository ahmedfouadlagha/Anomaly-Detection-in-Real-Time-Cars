# preprocessing/preprocess_data.py

import json
import pandas as pd
import os

# File paths
RAW_DATA_FILE = "mqtt/received_data.log"
PROCESSED_DATA_FILE = "data/processed/processed_data.csv"

# Preprocessing function
def preprocess_data():
    if not os.path.exists(RAW_DATA_FILE):
        print(f"Raw data file not found: {RAW_DATA_FILE}")
        return

    try:
        # Read raw data
        print("Reading raw data...")
        with open(RAW_DATA_FILE, "r") as file:
            raw_data = [json.loads(line.strip()) for line in file.readlines()]

        # Convert to DataFrame
        print("Converting data to DataFrame...")
        df = pd.DataFrame(raw_data)

        # Check for missing values
        print("Checking for missing values...")
        if df.isnull().any().sum() > 0:
            print("Filling missing values...")
            df.fillna(method="ffill", inplace=True)  # Forward-fill missing values

        # Add derived features (e.g., speed difference, temperature normalized)
        print("Adding derived features...")
        df["speed_diff"] = df["speed"].diff().fillna(0)  # Speed change
        df["temp_normalized"] = (df["engine_temp"] - df["engine_temp"].mean()) / df["engine_temp"].std()

        # Save processed data
        print("Saving processed data...")
        os.makedirs(os.path.dirname(PROCESSED_DATA_FILE), exist_ok=True)
        df.to_csv(PROCESSED_DATA_FILE, index=False)
        print(f"Processed data saved to {PROCESSED_DATA_FILE}")
    except Exception as e:
        print(f"Error during preprocessing: {e}")

if __name__ == "__main__":
    preprocess_data()
