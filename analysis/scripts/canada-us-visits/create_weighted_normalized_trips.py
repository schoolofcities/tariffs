from pathlib import Path

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = ANALYSIS_DIR.parent


def load_normalized_inputs() -> pd.DataFrame:
    papa_path = PROJECT_ROOT / "static" / "canada-us-visits" / "us_normalized_trips.csv"
    sierra_path = PROJECT_ROOT / "static" / "canada-us-visits" / "us_normalized_trips_v2.csv"

    papa = pd.read_csv(papa_path, usecols=["METRO", "DATE", "normalized"])
    sierra = pd.read_csv(sierra_path, usecols=["METRO", "DATE", "normalized"])

    papa = papa.rename(columns={"normalized": "normalized_papa"})
    sierra = sierra.rename(columns={"normalized": "normalized_sierra"})

    for frame in (papa, sierra):
        frame["DATE"] = frame["DATE"].astype(str).str.strip()
        frame["METRO"] = frame["METRO"].astype(str).str.strip()

    merged = papa.merge(sierra, on=["METRO", "DATE"], how="left")
    return merged


def load_daily_devices() -> pd.DataFrame:
    papa_devices_path = ANALYSIS_DIR / "raw" / "daily_can_total_papa.csv"
    sierra_devices_path = ANALYSIS_DIR / "raw" / "daily_can_total_sierra.csv"

    papa_devices = pd.read_csv(papa_devices_path, usecols=["SNAPSHOT_EVENT_DATE", "UNIQUE_CANADIAN_DEVICES"])
    sierra_devices = pd.read_csv(sierra_devices_path, usecols=["SNAPSHOT_EVENT_DATE", "UNIQUE_CANADIAN_DEVICES"])

    papa_devices = papa_devices.rename(
        columns={
            "SNAPSHOT_EVENT_DATE": "DATE",
            "UNIQUE_CANADIAN_DEVICES": "unique_devices_papa",
        }
    )
    sierra_devices = sierra_devices.rename(
        columns={
            "SNAPSHOT_EVENT_DATE": "DATE",
            "UNIQUE_CANADIAN_DEVICES": "unique_devices_sierra",
        }
    )

    for frame in (papa_devices, sierra_devices):
        frame["DATE"] = frame["DATE"].astype(str).str.strip()

    return papa_devices.merge(sierra_devices, on="DATE", how="left")


def build_weighted_series() -> pd.DataFrame:
    normalized = load_normalized_inputs()
    daily_devices = load_daily_devices()

    merged = normalized.merge(daily_devices, on="DATE", how="inner")

    merged["unique_devices_sierra"] = merged["unique_devices_sierra"].fillna(0)
    merged["normalized_sierra"] = merged["normalized_sierra"].fillna(merged["normalized_papa"])

    merged["total_devices"] = merged["unique_devices_papa"] + merged["unique_devices_sierra"]
    merged = merged[merged["total_devices"] > 0].copy()

    merged["weight_papa"] = merged["unique_devices_papa"] / merged["total_devices"]
    merged["weight_sierra"] = merged["unique_devices_sierra"] / merged["total_devices"]

    merged["normalized"] = (
        merged["normalized_papa"] * merged["weight_papa"]
        + merged["normalized_sierra"] * merged["weight_sierra"]
    )

    output = merged[["METRO", "DATE", "normalized"]].copy()
    output = output.sort_values(["DATE", "METRO"]).reset_index(drop=True)
    return output


def main() -> None:
    weighted = build_weighted_series()

    output_path = PROJECT_ROOT / "static" / "canada-us-visits" / "us_normalized_trips_weighted.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    weighted.to_csv(output_path, index=False)

    print(f"Wrote {len(weighted)} rows to {output_path} using per-day weights derived from device counts.")


if __name__ == "__main__":
    main()
