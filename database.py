
import sqlite3
import pandas as pd
from pathlib import Path


def save_telemetry(
    df: pd.DataFrame,
    db_path: str = "data/solarwatch.db"
):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "timestamp",
        "voltage",
        "current",
        "solar_power",
        "load_power",
        "battery_soc",
        "temperature",
        "interval_hours",
        "battery_power_w",
        "solar_energy_wh",
        "load_energy_wh",
        "battery_energy_wh",
        "solar_load_balance_w"
    ]

    missing = [col for col in columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing database columns: {missing}")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS telemetry (
        timestamp TEXT NOT NULL,
        voltage REAL,
        current REAL,
        solar_power REAL,
        load_power REAL,
        battery_soc REAL,
        temperature REAL,
        interval_hours REAL,
        battery_power_w REAL,
        solar_energy_wh REAL,
        load_energy_wh REAL,
        battery_energy_wh REAL,
        solar_load_balance_w REAL
    );
    """

    connection = sqlite3.connect(path)

    try:
        cursor = connection.cursor()

        cursor.execute(create_table_query)

        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_telemetry_timestamp
            ON telemetry(timestamp);
        """)

        update_columns = [
            col for col in columns if col != "timestamp"
        ]

        update_clause = ", ".join(
            f"{col} = excluded.{col}"
            for col in update_columns
        )

        placeholders = ", ".join(["?"] * len(columns))
        column_names = ", ".join(columns)

        upsert_query = f"""
        INSERT INTO telemetry ({column_names})
        VALUES ({placeholders})
        ON CONFLICT(timestamp) DO UPDATE SET
        {update_clause};
        """

        records_df = df[columns].copy()

        records_df["timestamp"] = (
            pd.to_datetime(records_df["timestamp"])
            .dt.strftime("%Y-%m-%d %H:%M:%S")
        )

        records = list(
            records_df.itertuples(index=False, name=None)
        )

        cursor.executemany(upsert_query, records)

        connection.commit()

        print(
            f"Successfully processed {len(records)} records "
            "using SQLite UPSERT."
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
