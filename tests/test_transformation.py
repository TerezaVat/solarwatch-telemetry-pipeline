
import unittest
import pandas as pd

from transformation import transform_telemetry


class TestTransformation(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "timestamp": [
                "2026-11-11 08:00:00",
                "2026-11-11 08:05:00",
                "2026-11-11 08:10:00"
            ],
            "voltage": [12.0, 12.0, 12.0],
            "current": [1.0, -1.0, 0.5],
            "solar_power": [0, 60, 120],
            "load_power": [30, 30, 30]
        })

    def test_first_interval_is_zero(self):
        result = transform_telemetry(self.df)

        self.assertEqual(result.loc[0, "interval_hours"], 0.0)

    def test_sampling_interval_is_five_minutes(self):
        result = transform_telemetry(self.df)

        expected = 5 / 60

        self.assertAlmostEqual(
            result.loc[1, "interval_hours"],
            expected
        )

    def test_battery_power_calculation(self):
        result = transform_telemetry(self.df)

        self.assertAlmostEqual(
            result.loc[0, "battery_power_w"],
            12.0
        )

        self.assertAlmostEqual(
            result.loc[1, "battery_power_w"],
            -12.0
        )

    def test_solar_energy_calculation(self):
        result = transform_telemetry(self.df)

        self.assertAlmostEqual(
            result.loc[1, "solar_energy_wh"],
            5.0
        )

    def test_duplicate_timestamps_raise_error(self):
        invalid_df = self.df.copy()
        invalid_df.loc[1, "timestamp"] = "2026-11-11 08:00:00"

        with self.assertRaises(ValueError):
            transform_telemetry(invalid_df)

    def test_missing_column_raises_error(self):
        invalid_df = self.df.drop(columns=["current"])

        with self.assertRaises(ValueError):
            transform_telemetry(invalid_df)


if __name__ == "__main__":
    unittest.main()
