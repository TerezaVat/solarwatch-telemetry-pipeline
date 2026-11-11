
"""
SOLARWATCH
Solar Energy Telemetry & Monitoring Pipeline
"""

from ingestion import load_telemetry


def main():
    print("=" * 45)
    print("SOLARWATCH TELEMETRY PIPELINE")
    print("=" * 45)

    df = load_telemetry("data/telemetry.csv")

    print("\nDataset preview:")
    print(df.head())

    print("\nDataset information:")
    df.info()


if __name__ == "__main__":
    main()
