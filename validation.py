
"""
SOLARWATCH - Data Validation Module

Checks the quality and consistency of solar telemetry data.
"""

import pandas as pd


def validate_telemetry(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate solar telemetry measurements.

    Returns:
        pd.DataFrame: Data quality validation report.
    """

    checks = []

    def add_check(name, status, details):
        checks.append({
            "check": name,
            "status": status,
            "details": details
        })

    # 1. Check required columns
    required_columns = [
        "timestamp",
        "voltage",
        "current",
        "solar_power",
        "load_power",
        "battery_soc",
        "temperature"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        add_check(
            "Required columns",
            "ERROR",
            f"Missing columns: {missing_columns}"
        )

        return pd.DataFrame(checks)

    add_check(
        "Required columns",
        "PASS",
        "All required columns are present."
    )

    # 2. Check missing values
    missing_values = int(df[required_columns].isna().sum().sum())

    add_check(
        "Missing values",
        "WARNING" if missing_values else "PASS",
        f"Found {missing_values} missing values."
    )

    # 3. Check duplicate timestamps
    duplicates = int(df["timestamp"].duplicated().sum())

    add_check(
        "Duplicate timestamps",
        "WARNING" if duplicates else "PASS",
        f"Found {duplicates} duplicate timestamps."
    )

    # 4. Check battery state of charge
    invalid_soc = int(
        (~df["battery_soc"].dropna().between(0, 100)).sum()
    )

    add_check(
        "Battery SOC range",
        "ERROR" if invalid_soc else "PASS",
        f"Found {invalid_soc} invalid SOC values."
    )

    # 5. Check solar power
    invalid_solar = int(
        (df["solar_power"].dropna() < 0).sum()
    )

    add_check(
        "Solar power",
        "ERROR" if invalid_solar else "PASS",
        f"Found {invalid_solar} negative solar power values."
    )

    # 6. Check load power
    invalid_load = int(
        (df["load_power"].dropna() < 0).sum()
    )

    add_check(
        "Load power",
        "ERROR" if invalid_load else "PASS",
        f"Found {invalid_load} negative load power values."
    )

    # 7. Check battery voltage
    invalid_voltage = int(
        (df["voltage"].dropna() <= 0).sum()
    )

    add_check(
        "Battery voltage",
        "ERROR" if invalid_voltage else "PASS",
        f"Found {invalid_voltage} invalid voltage values."
    )

    return pd.DataFrame(checks)
