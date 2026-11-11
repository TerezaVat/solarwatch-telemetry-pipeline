
"""
SOLARWATCH
Solar Energy Telemetry & Monitoring Pipeline
"""

from ingestion import load_telemetry
from validation import validate_telemetry
from transformation import transform_telemetry


def main():

    print("=" * 50)
    print("SOLARWATCH TELEMETRY PIPELINE")
    print("=" * 50)

    # STEP 1: DATA INGESTION
    df = load_telemetry("data/telemetry.csv")

    print("\nDATASET PREVIEW")
    print(df.head())

    # STEP 2: DATA VALIDATION
    print("\nDATA QUALITY REPORT")
    print("-" * 50)

    report = validate_telemetry(df)
    print(report.to_string(index=False))

    errors = (report["status"] == "ERROR").sum()
    warnings = (report["status"] == "WARNING").sum()

    print("\nVALIDATION SUMMARY")
    print(f"Errors: {errors}")
    print(f"Warnings: {warnings}")

    if errors > 0:
        print("Data validation failed. Transformation skipped.")
        return

    print("Data validation completed successfully.")

    # STEP 3: DATA TRANSFORMATION
    print("\nENERGY TRANSFORMATION")
    print("-" * 50)

    transformed_df = transform_telemetry(df)

    columns = [
        "timestamp",
        "battery_power_w",
        "solar_energy_wh",
        "load_energy_wh",
        "battery_energy_wh",
        "solar_load_balance_w"
    ]

    print(
        transformed_df[columns]
        .round(2)
        .to_string(index=False, col_space=15)
    )

    # STEP 4: ENERGY SUMMARY
    print("\nENERGY SUMMARY")

    print(
        f"Total solar energy: "
        f"{transformed_df['solar_energy_wh'].sum():.2f} Wh"
    )

    print(
        f"Total load energy: "
        f"{transformed_df['load_energy_wh'].sum():.2f} Wh"
    )

    print(
        f"Net battery energy (positive = discharge): "
        f"{transformed_df['battery_energy_wh'].sum():.2f} Wh"
    )


if __name__ == "__main__":
    main()
