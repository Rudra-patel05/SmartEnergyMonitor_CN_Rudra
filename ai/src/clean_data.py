"""
Clean Data Module
=================
Performs comprehensive data quality checks, identifies & excludes test/duplicate
records, validates numerical ranges, and produces a pristine dataset for ML
without modifying the original database.
"""

import os
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def check_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes and returns a comprehensive data quality dictionary.
    """
    total_rows = len(df)
    missing_vals = df.isnull().sum().to_dict()
    
    # Duplicates across (device_id, timestamp)
    duplicate_rows = df.duplicated(subset=["device_id", "timestamp"], keep=False).sum()
    duplicate_exact = df.duplicated(subset=["device_id", "timestamp", "voltage", "current", "power", "energy"]).sum()

    # Range and numerical validity checks
    invalid_voltage = ((df["voltage"] < 150) | (df["voltage"] > 300)).sum()
    invalid_current = (df["current"] < 0).sum()
    invalid_power = (df["power"] < 0).sum()
    invalid_energy = (df["energy"] < 0).sum()
    invalid_temp = ((df["temperature"] < -10) | (df["temperature"] > 60)).sum()
    invalid_occupancy = (df["occupancy"] < 0).sum()

    # Per device and area breakdown
    device_counts = df["device_id"].value_counts().to_dict()
    area_counts = df["area"].value_counts().to_dict()

    # Min/Max metrics
    metrics = {
        "total_rows": total_rows,
        "missing_values": missing_vals,
        "duplicate_records_device_ts": int(duplicate_rows),
        "exact_duplicate_rows": int(duplicate_exact),
        "invalid_counts": {
            "voltage_out_of_range": int(invalid_voltage),
            "negative_current": int(invalid_current),
            "negative_power": int(invalid_power),
            "negative_energy": int(invalid_energy),
            "temperature_out_of_range": int(invalid_temp),
            "negative_occupancy": int(invalid_occupancy),
        },
        "voltage_range": (float(df["voltage"].min()), float(df["voltage"].max())),
        "current_range": (float(df["current"].min()), float(df["current"].max())),
        "power_range": (float(df["power"].min()), float(df["power"].max())),
        "energy_range": (float(df["energy"].min()), float(df["energy"].max())),
        "temperature_range": (float(df["temperature"].min()), float(df["temperature"].max())),
        "occupancy_range": (int(df["occupancy"].min()), int(df["occupancy"].max())),
        "timestamp_range": (str(df["timestamp"].min()), str(df["timestamp"].max())),
        "records_per_device": device_counts,
        "records_per_area": area_counts,
    }
    return metrics


def print_quality_report(report: Dict[str, Any], title: str = "DATA QUALITY REPORT") -> None:
    """
    Prints a nicely formatted report of the data quality metrics.
    """
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print(f"Total Rows:               {report['total_rows']}")
    print(f"Duplicate (Device+TS):    {report['duplicate_records_device_ts']}")
    print(f"Exact Duplicate Rows:     {report['exact_duplicate_rows']}")
    print(f"Timestamp Range:          {report['timestamp_range'][0]}  -->  {report['timestamp_range'][1]}")
    
    print("\nMissing Values:")
    for col, count in report['missing_values'].items():
        print(f"  - {col:<15}: {count}")

    print("\nValue Ranges:")
    print(f"  - Voltage (V):          [{report['voltage_range'][0]:.2f}, {report['voltage_range'][1]:.2f}]")
    print(f"  - Current (A):          [{report['current_range'][0]:.2f}, {report['current_range'][1]:.2f}]")
    print(f"  - Power (W):            [{report['power_range'][0]:.2f}, {report['power_range'][1]:.2f}]")
    print(f"  - Energy (kWh):         [{report['energy_range'][0]:.4f}, {report['energy_range'][1]:.4f}]")
    print(f"  - Temperature (°C):     [{report['temperature_range'][0]:.1f}, {report['temperature_range'][1]:.1f}]")
    print(f"  - Occupancy (persons):  [{report['occupancy_range'][0]}, {report['occupancy_range'][1]}]")

    print("\nInvalid Value Counts:")
    for k, v in report['invalid_counts'].items():
        print(f"  - {k:<25}: {v}")

    print("\nRecords per Device:")
    for dev, count in report['records_per_device'].items():
        print(f"  - {dev:<10}: {count} records")

    print("\nRecords per Area:")
    for area, count in report['records_per_area'].items():
        print(f"  - {area:<25}: {count} records")
    print("=" * 70 + "\n")


def clean_energy_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cleans raw energy data:
      1. Identifies test fixtures (e.g. test_api endpoint testing entries).
      2. Removes exact and duplicate timestamp test entries.
      3. Validates range bounds.
      4. Standardizes data types and datetime format.
      5. Sorts chronologically per device.

    Returns:
      (cleaned_df, excluded_test_df)
    """
    df_clean = df.copy()

    # Identify test records:
    # 1) API test fixture records: LAB-01 with hardcoded timestamp 2026-08-23 10:00:00 and power 2351.1
    is_test_fixture = (
        (df_clean["device_id"] == "LAB-01") & 
        (df_clean["timestamp"] == "2026-08-23 10:00:00") & 
        (df_clean["power"] == 2351.1)
    )

    # 2) Duplicate timestamp records for same device
    is_duplicate_ts = df_clean.duplicated(subset=["device_id", "timestamp"], keep="first")

    # Combine test exclusions
    test_mask = is_test_fixture | is_duplicate_ts

    excluded_test_df = df_clean[test_mask].copy()
    cleaned_df = df_clean[~test_mask].copy()

    # Ensure correct data types
    cleaned_df["timestamp"] = pd.to_datetime(cleaned_df["timestamp"])
    cleaned_df["voltage"] = cleaned_df["voltage"].astype(float)
    cleaned_df["current"] = cleaned_df["current"].astype(float)
    cleaned_df["power"] = cleaned_df["power"].astype(float)
    cleaned_df["energy"] = cleaned_df["energy"].astype(float)
    cleaned_df["temperature"] = cleaned_df["temperature"].astype(float)
    cleaned_df["occupancy"] = cleaned_df["occupancy"].astype(int)

    # Filter out invalid records if any
    valid_mask = (
        (cleaned_df["voltage"] > 0) &
        (cleaned_df["current"] >= 0) &
        (cleaned_df["power"] >= 0) &
        (cleaned_df["energy"] >= 0) &
        (cleaned_df["occupancy"] >= 0)
    )
    cleaned_df = cleaned_df[valid_mask]

    # Sort chronologically by device and timestamp
    cleaned_df = cleaned_df.sort_values(by=["device_id", "timestamp"]).reset_index(drop=True)

    return cleaned_df, excluded_test_df


if __name__ == "__main__":
    from load_data import load_raw_data_from_db
    
    print("=" * 70)
    print("  AI DATA CLEANING & QUALITY VALIDATION")
    print("=" * 70)
    
    raw_df = load_raw_data_from_db()
    raw_report = check_data_quality(raw_df)
    print_quality_report(raw_report, title="RAW DATA QUALITY REPORT")

    cleaned_df, excluded_df = clean_energy_data(raw_df)
    print(f"\n[CLEANING SUMMARY]")
    print(f"Raw Records:            {len(raw_df)}")
    print(f"Excluded Test Records:  {len(excluded_df)}")
    print(f"Cleaned Records:        {len(cleaned_df)}")

    if len(excluded_df) > 0:
        print("\nExcluded Test Records Sample:")
        print(excluded_df[["id", "device_id", "timestamp", "power", "energy", "occupancy"]])

    clean_report = check_data_quality(cleaned_df)
    print_quality_report(clean_report, title="CLEANED DATA QUALITY REPORT")
