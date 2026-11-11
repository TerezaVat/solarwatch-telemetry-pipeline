
"""
SOLARWATCH
Solar Energy Telemetry & Monitoring Pipeline
"""

from ingestion import load_telemetry
from validation import validate_telemetry


def main():

    print("=" * 50)
    print("SOLARWATCH TELEMETRY PIPELINE")
    print("=" * 50)

    # Step 1: Load telemetry data
    df = load_telemetry("data/telemetry.csv")

    print("\nDataset preview:")
    print(df.head())

    # Step 2: Validate telemetry data
    print("\nDATA QUALITY REPORT")
    print("-" * 50)

    report = validate_telemetry(df)

    print(report.to_string(index=False))

    # Step 3: Display validation summary
    errors = (report["status"] == "ERROR").sum()
    warnings = (report["status"] == "WARNING").sum()

    print("\nVALIDATION SUMMARY")
    print(f"Errors: {errors}")
    print(f"Warnings: {warnings}")

    if errors == 0:
        print("Data validation completed successfully.")
    else:
        print("Data validation detected errors.")


if __name__ == "__main__":
    main()
