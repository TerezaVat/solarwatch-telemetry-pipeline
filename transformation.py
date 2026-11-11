
"""
SOLARWATCH - Data Transformation Module

Transforms raw solar telemetry into
engineering and energy performance metrics.
"""

import pandas as pd


def transform_telemetry(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate derived power and energy metrics.

    Positive battery current = discharge.
    Negative battery current = charging.

    Each record represents the interval ending
    at its timestamp.
    """

    required_columns = [
        "timestamp",
        "voltage",
        "current",
        "solar_power",
        "load_power"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    result = df.copy()

    result["timestamp"] = pd.to_datetime(
        result["timestamp"]
    )

    result = result.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    # Calculate measurement intervals in hours
    intervals = (
        result["timestamp"]
        .diff()
        .dt.total_seconds() / 3600
    )

    # Check for duplicate or non-increasing timestamps
    if intervals.iloc[1:].le(0).any():
        raise ValueError(
            "Duplicate or invalid timestamps detected."
        )

    # The first measurement has no preceding interval
    result["interval_hours"] = intervals.fillna(0.0)

    # Calculate battery power
    result["battery_power_w"] = (
        result["voltage"] * result["current"]
    )

    # Calculate energy per measurement interval
    result["solar_energy_wh"] = (
        result["solar_power"] *
        result["interval_hours"]
    )

    result["load_energy_wh"] = (
        result["load_power"] *
        result["interval_hours"]
    )

    result["battery_energy_wh"] = (
        result["battery_power_w"] *
        result["interval_hours"]
    )

    # Positive = solar generation exceeds load
    result["solar_load_balance_w"] = (
        result["solar_power"] -
        result["load_power"]
    )

    return result
