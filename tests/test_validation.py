
"""
SOLARWATCH - Data Validation Tests

Tests whether the validation module detects
incorrect solar telemetry measurements.
"""

import unittest
import pandas as pd

from ingestion import load_telemetry
from validation import validate_telemetry


class TestTelemetryValidation(unittest.TestCase):

    def setUp(self):
        self.df = load_telemetry("data/telemetry.csv")

    def get_status(self, report, check_name):
        result = report.loc[
            report["check"] == check_name, "status"
        ]
        return result.iloc[0]

    def test_invalid_battery_soc(self):
        df = self.df.copy()
        df.loc[0, "battery_soc"] = 140

        report = validate_telemetry(df)

        self.assertEqual(
            self.get_status(report, "Battery SOC range"),
            "ERROR"
        )

    def test_negative_solar_power(self):
        df = self.df.copy()
        df.loc[0, "solar_power"] = -50

        report = validate_telemetry(df)

        self.assertEqual(
            self.get_status(report, "Solar power"),
            "ERROR"
        )

    def test_duplicate_timestamp(self):
        df = self.df.copy()
        df.loc[1, "timestamp"] = df.loc[0, "timestamp"]

        report = validate_telemetry(df)

        self.assertEqual(
            self.get_status(report, "Duplicate timestamps"),
            "WARNING"
        )

    def test_missing_temperature(self):
        df = self.df.copy()
        df.loc[0, "temperature"] = float("nan")

        report = validate_telemetry(df)

        self.assertEqual(
            self.get_status(report, "Missing values"),
            "WARNING"
        )


if __name__ == "__main__":
    unittest.main()
