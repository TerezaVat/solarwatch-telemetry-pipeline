
"""
SOLARWATCH - Data Ingestion Module

Loads solar telemetry data from CSV files.
"""

import pandas as pd
from pathlib import Path


def load_telemetry(file_path: str) -> pd.DataFrame:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Telemetry file not found: {path}"
        )

    df = pd.read_csv(path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    print(f"Successfully loaded {len(df)} records.")

    return df
