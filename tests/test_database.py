
import unittest
import sqlite3
import tempfile
from pathlib import Path

import pandas as pd

from database import save_telemetry


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"

        self.df = pd.DataFrame({
            "timestamp": pd.to_datetime([
                "2026-11-11 08:00:00",
                "2026-11-11 08:05:00"
            ]),
            "voltage": [12.8, 13.0],
            "current": [2.0, -1.0],
            "solar_power": [50, 70],
            "load_power": [45, 45],
            "battery_soc": [72.0, 72.1],
            "temperature": [18.5, 19.0],
            "interval_hours": [0.0, 5 / 60],
            "battery_power_w": [25.6, -13.0],
            "solar_energy_wh": [0.0, 5.83],
            "load_energy_wh": [0.0, 3.75],
            "battery_energy_wh": [0.0, -1.08],
            "solar_load_balance_w": [5, 25]
        })

    def tearDown(self):
        self.temp_dir.cleanup()

    # TEST 1: Database file creation
    def test_database_file_is_created(self):
        save_telemetry(self.df, str(self.db_path))

        self.assertTrue(self.db_path.exists())

    # TEST 2: Record count
    def test_all_records_are_saved(self):
        save_telemetry(self.df, str(self.db_path))

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM telemetry")
        count = cursor.fetchone()[0]

        connection.close()

        self.assertEqual(count, 2)

    # TEST 3: Transformed columns
    def test_transformed_columns_are_saved(self):
        save_telemetry(self.df, str(self.db_path))

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("PRAGMA table_info(telemetry)")
        columns = [row[1] for row in cursor.fetchall()]

        connection.close()

        self.assertIn("battery_power_w", columns)
        self.assertIn("solar_energy_wh", columns)
        self.assertIn("battery_energy_wh", columns)

    # TEST 4: No duplicate records after repeated insertion
    def test_repeated_insert_does_not_duplicate_records(self):
        save_telemetry(self.df, str(self.db_path))
        save_telemetry(self.df, str(self.db_path))

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM telemetry")
        count = cursor.fetchone()[0]

        connection.close()

        self.assertEqual(count, 2)

    # TEST 5: Existing record is updated
    def test_existing_record_is_updated(self):
        save_telemetry(self.df, str(self.db_path))

        updated_df = self.df.copy()
        updated_df.loc[0, "solar_power"] = 100

        save_telemetry(updated_df, str(self.db_path))

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT solar_power
            FROM telemetry
            WHERE timestamp = ?
            """,
            ("2026-11-11 08:00:00",)
        )

        solar_power = cursor.fetchone()[0]

        connection.close()

        self.assertEqual(solar_power, 100)


if __name__ == "__main__":
    unittest.main()
