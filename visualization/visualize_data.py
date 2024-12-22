# visualization/visualize_data.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File path for the processed data
PROCESSED_DATA_FILE = "data/processed/processed_data.csv"

def visualize_data():
    if not os.path.exists(PROCESSED_DATA_FILE):
        print(f"Processed data file not found: {PROCESSED_DATA_FILE}")
        return

    try:
        # Load the processed data
        print("Loading processed data...")
        df = pd.read_csv(PROCESSED_DATA_FILE)

        # Display basic statistics
        print("Data Statistics:")
        print(df.describe())

        # Plot histograms for numeric columns
        print("Creating histograms...")
        numeric_columns = ["speed", "engine_temp", "speed_diff", "temp_normalized"]
        for col in numeric_columns:
            plt.figure()
            sns.histplot(df[col], kde=True, bins=20)
            plt.title(f"Histogram of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.savefig(f"visualization/{col}_histogram.png")  # Save plot
            plt.show()

        # Scatter plot: Speed vs Engine Temperature
        print("Creating scatter plot for Speed vs Engine Temperature...")
        plt.figure()
        sns.scatterplot(x=df["speed"], y=df["engine_temp"], hue=df["car_id"], palette="viridis", legend=None)
        plt.title("Speed vs Engine Temperature")
        plt.xlabel("Speed (km/h)")
        plt.ylabel("Engine Temperature (°C)")
        plt.savefig("visualization/speed_vs_temp_scatter.png")  # Save plot
        plt.show()

        # Line chart: Speed over time for each car
        print("Creating line chart for Speed over Time...")
        plt.figure(figsize=(10, 6))
        for car_id in df["car_id"].unique():
            car_data = df[df["car_id"] == car_id]
            plt.plot(car_data["timestamp"], car_data["speed"], label=car_id)
        plt.title("Speed Over Time (for each car)")
        plt.xlabel("Timestamp")
        plt.ylabel("Speed (km/h)")
        plt.legend(loc="upper right", fontsize="small")
        plt.savefig("visualization/speed_over_time_linechart.png")  # Save plot
        plt.show()

        print("Visualizations complete. Check the 'visualization/' directory for saved plots.")

    except Exception as e:
        print(f"Error during visualization: {e}")

if __name__ == "__main__":
    visualize_data()
