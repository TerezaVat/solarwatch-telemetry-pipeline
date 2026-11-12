
"""
SOLARWATCH
Solar Energy Telemetry Visualization
"""

import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


DB_PATH = "data/solarwatch.db"
REPORTS_DIR = Path("reports")


def load_visualization_data(db_path=DB_PATH):
    """Load telemetry data directly from SQLite."""

    connection = sqlite3.connect(db_path)

    try:
        query = """
        SELECT
            timestamp,
            solar_power,
            load_power,
            battery_soc,
            battery_power_w
        FROM telemetry
        ORDER BY timestamp;
        """

        df = pd.read_sql_query(query, connection)

        if df.empty:
            raise ValueError("No telemetry data available for visualization.")

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        return df

    finally:
        connection.close()


def setup_time_axis(ax):
    """Format the time axis."""

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%H:%M")
    )

    ax.xaxis.set_major_locator(
        mdates.AutoDateLocator()
    )

    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")


def plot_solar_vs_load(df):
    """Compare solar generation and load power."""

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df["timestamp"],
        df["solar_power"],
        marker="o",
        label="Solar Power"
    )

    ax.plot(
        df["timestamp"],
        df["load_power"],
        marker="s",
        label="Load Power"
    )

    ax.set_title("Solar Generation vs Load Consumption")
    ax.set_xlabel("Time")
    ax.set_ylabel("Power (W)")

    ax.legend()
    ax.grid(True, alpha=0.3)

    setup_time_axis(ax)

    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "solar_vs_load_power.png", dpi=150)
    plt.close(fig)


def plot_battery_soc(df):
    """Visualize battery State of Charge."""

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df["timestamp"],
        df["battery_soc"],
        marker="o",
        label="Battery SOC"
    )

    ax.set_title("Battery State of Charge")
    ax.set_xlabel("Time")
    ax.set_ylabel("State of Charge (%)")

    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(True, alpha=0.3)

    setup_time_axis(ax)

    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "battery_soc.png", dpi=150)
    plt.close(fig)


def plot_battery_power(df):
    """Visualize battery charging and discharging."""

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df["timestamp"],
        df["battery_power_w"],
        marker="o",
        label="Battery Power"
    )

    ax.axhline(y=0, linestyle="--", linewidth=1)

    ax.set_title("Battery Charging and Discharging")
    ax.set_xlabel("Time")
    ax.set_ylabel("Battery Power (W)")

    ax.legend()
    ax.grid(True, alpha=0.3)

    setup_time_axis(ax)

    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "battery_power.png", dpi=150)
    plt.close(fig)


def generate_visualizations(db_path=DB_PATH):
    """Generate all SOLARWATCH visualization reports."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("\nGENERATING VISUALIZATIONS")
    print("-" * 50)

    df = load_visualization_data(db_path)

    plot_solar_vs_load(df)
    print("Generated: solar_vs_load_power.png")

    plot_battery_soc(df)
    print("Generated: battery_soc.png")

    plot_battery_power(df)
    print("Generated: battery_power.png")

    print("\nAll visualizations generated successfully.")


if __name__ == "__main__":
    generate_visualizations()
