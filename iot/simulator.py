#!/usr/bin/env python3
"""
Virtual IoT Energy Meter Simulator
===================================

Generates simulated energy consumption data for campus areas.
All data is SIMULATED — no physical sensors or hardware are used.

Usage:
    python iot/simulator.py                         # Default: 100 readings per device
    python iot/simulator.py --readings 200          # 200 readings per device
    python iot/simulator.py --readings 50 --interval 600   # 50 readings, 10-min intervals

Output Files:
    iot/data/energy_readings.csv
    iot/data/energy_readings.json
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Add the script's directory to the path so imports work
# regardless of where the script is called from
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    DEVICE_CONFIGS,
    DEFAULT_READINGS_PER_DEVICE,
    DEFAULT_INTERVAL_SECONDS,
    CSV_OUTPUT_PATH,
    JSON_OUTPUT_PATH,
)
from devices import VirtualEnergyMeter
from api_client import ApiClient


# ============================================================
# Validation
# ============================================================

def validate_reading(reading: Dict[str, Any]) -> bool:
    """
    Validate that a single energy reading has sensible values.

    Checks:
      - voltage > 0
      - current >= 0
      - power >= 0
      - energy >= 0
      - occupancy >= 0
      - timestamp is a valid datetime string

    Args:
        reading: Dictionary containing one energy reading

    Returns:
        True if all checks pass, False otherwise
    """
    errors: List[str] = []

    if reading["voltage"] <= 0:
        errors.append(f"Voltage must be > 0, got {reading['voltage']}")

    if reading["current"] < 0:
        errors.append(f"Current must be >= 0, got {reading['current']}")

    if reading["power"] < 0:
        errors.append(f"Power must be >= 0, got {reading['power']}")

    if reading["energy"] < 0:
        errors.append(f"Energy must be >= 0, got {reading['energy']}")

    if reading["occupancy"] < 0:
        errors.append(f"Occupancy must be >= 0, got {reading['occupancy']}")

    # Validate timestamp format
    try:
        datetime.strptime(reading["timestamp"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        errors.append(f"Invalid timestamp format: {reading['timestamp']}")

    # Report errors
    if errors:
        for error in errors:
            print(f"  [VALIDATION ERROR] {reading['device_id']}: {error}")
        return False

    return True


# ============================================================
# File Output
# ============================================================

def save_to_csv(readings: List[Dict[str, Any]], filepath: str) -> None:
    """
    Save all readings to a CSV file.

    Creates the output directory if it does not exist.

    Args:
        readings: List of energy reading dictionaries
        filepath: Full path to the output CSV file
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    fieldnames = [
        "device_id", "area", "timestamp", "voltage",
        "current", "power", "energy", "temperature", "occupancy",
    ]

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(readings)
        print(f"  CSV saved : {filepath} ({len(readings)} records)")
    except IOError as e:
        print(f"  [ERROR] Failed to write CSV: {e}")
        raise


def save_to_json(readings: List[Dict[str, Any]], filepath: str) -> None:
    """
    Save all readings to a JSON file with metadata.

    Creates the output directory if it does not exist.
    The JSON includes a metadata section and the readings array.

    Args:
        readings: List of energy reading dictionaries
        filepath: Full path to the output JSON file
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    output = {
        "metadata": {
            "project": "Smart Energy Monitor – Smart Campus",
            "description": "Simulated IoT energy readings (no physical sensors)",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_records": len(readings),
            "devices": sorted(set(r["device_id"] for r in readings)),
            "areas": sorted(set(r["area"] for r in readings)),
        },
        "readings": readings,
    }

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"  JSON saved: {filepath} ({len(readings)} records)")
    except IOError as e:
        print(f"  [ERROR] Failed to write JSON: {e}")
        raise


# ============================================================
# Display
# ============================================================

def print_sample_readings(readings: List[Dict[str, Any]], count: int = 5) -> None:
    """
    Print the first N readings in a formatted table.

    Args:
        readings: List of energy reading dictionaries
        count:    Number of sample readings to display
    """
    print(f"\n{'=' * 130}")
    print(f"  SAMPLE READINGS (first {count})")
    print(f"{'=' * 130}")

    header = (
        f"  {'Device':<10} {'Area':<25} {'Timestamp':<22}"
        f"{'Voltage':>9} {'Current':>9} {'Power':>11}"
        f"{'Energy':>10} {'Temp':>7} {'Occ':>5}"
    )
    print(header)
    print(f"  {'-' * 126}")

    for reading in readings[:count]:
        row = (
            f"  {reading['device_id']:<10} "
            f"{reading['area']:<25} "
            f"{reading['timestamp']:<22}"
            f"{reading['voltage']:>7.1f} V "
            f"{reading['current']:>7.2f} A "
            f"{reading['power']:>9.2f} W "
            f"{reading['energy']:>8.4f} kWh"
            f"{reading['temperature']:>5.1f} °C"
            f"{reading['occupancy']:>4d}"
        )
        print(row)

    print(f"{'=' * 130}")


def print_summary_per_device(readings: List[Dict[str, Any]]) -> None:
    """
    Print a summary of readings grouped by device.

    Shows total readings, min/max/avg power, and total energy per device.

    Args:
        readings: List of energy reading dictionaries
    """
    # Group readings by device_id
    devices: Dict[str, List[Dict[str, Any]]] = {}
    for r in readings:
        devices.setdefault(r["device_id"], []).append(r)

    print(f"\n{'=' * 90}")
    print(f"  PER-DEVICE SUMMARY")
    print(f"{'=' * 90}")
    print(
        f"  {'Device':<10} {'Area':<25} {'Readings':>8}"
        f"  {'Min Power':>10} {'Max Power':>10} {'Avg Power':>10}"
        f"  {'Total Energy':>12}"
    )
    print(f"  {'-' * 86}")

    for device_id in sorted(devices.keys()):
        device_readings = devices[device_id]
        area = device_readings[0]["area"]
        powers = [r["power"] for r in device_readings]
        total_energy = device_readings[-1]["energy"]  # Cumulative

        print(
            f"  {device_id:<10} {area:<25} {len(device_readings):>8}"
            f"  {min(powers):>9.2f}W {max(powers):>9.2f}W {sum(powers)/len(powers):>9.2f}W"
            f"  {total_energy:>10.4f} kWh"
        )

    print(f"{'=' * 90}")


# ============================================================
# Main Simulator
# ============================================================

def main() -> None:
    """Main entry point for the Virtual IoT Energy Meter Simulator."""

    # --- Parse command-line arguments ---
    parser = argparse.ArgumentParser(
        description="Virtual IoT Energy Meter Simulator — Generates simulated campus energy data",
        epilog="All data is SIMULATED. No physical sensors are used.",
    )
    parser.add_argument(
        "--readings",
        type=int,
        default=DEFAULT_READINGS_PER_DEVICE,
        help=f"Number of readings per device (default: {DEFAULT_READINGS_PER_DEVICE})",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_SECONDS,
        help=f"Interval between readings in seconds (default: {DEFAULT_INTERVAL_SECONDS})",
    )
    parser.add_argument(
        "--send-api",
        action="store_true",
        help="Send generated readings to the backend API",
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default="http://127.0.0.1:8000",
        help="Base URL of the backend API (default: http://127.0.0.1:8000)",
    )
    args = parser.parse_args()

    # --- Print banner ---
    print()
    print("=" * 60)
    print("  VIRTUAL IoT ENERGY METER SIMULATOR")
    print("  Smart Energy Monitor – Smart Campus (GTU PBL)")
    print("  All data is SIMULATED (no physical sensors)")
    print("=" * 60)
    print(f"\n  Configuration:")
    print(f"    Readings per device : {args.readings}")
    print(f"    Interval            : {args.interval} seconds ({args.interval / 60:.1f} min)")
    print(f"    Total devices       : {len(DEVICE_CONFIGS)}")
    print(f"    Total readings      : {args.readings * len(DEVICE_CONFIGS)}")
    print(f"    Time span           : {args.readings * args.interval / 3600:.1f} hours per device")
    print()

    # --- Generate readings for all devices ---
    all_readings: List[Dict[str, Any]] = []
    validation_errors: int = 0

    for device_config in DEVICE_CONFIGS:
        device_id = device_config["device_id"]
        area = device_config["area"]
        print(f"  Generating data for {device_id} ({area})...")

        # Create a virtual meter and generate readings
        meter = VirtualEnergyMeter(device_config)
        readings = meter.generate_readings(args.readings, args.interval)

        # Validate every reading
        for reading in readings:
            if not validate_reading(reading):
                validation_errors += 1

        all_readings.extend(readings)
        print(f"    -> {len(readings)} readings generated")

    # --- Sort all readings chronologically ---
    all_readings.sort(key=lambda r: (r["timestamp"], r["device_id"]))

    print(f"\n  Total readings generated : {len(all_readings)}")
    print(f"  Validation errors        : {validation_errors}")

    # --- Send to API if requested ---
    if args.send_api:
        print(f"\n  Sending {len(all_readings)} readings to API at {args.api_url}...")
        client = ApiClient(base_url=args.api_url)
        
        # Send in bulk
        api_success = 0
        api_failed = 0
        
        success = client.send_bulk_readings(all_readings)
        if success:
            api_success = len(all_readings)
        else:
            api_failed = len(all_readings)
            
        print(f"    Sent: {len(all_readings)}")
        print(f"    Successful: {api_success}")
        print(f"    Failed: {api_failed}")

    # --- Save output files ---
    print("\n  Saving output files...")
    try:
        save_to_csv(all_readings, CSV_OUTPUT_PATH)
        save_to_json(all_readings, JSON_OUTPUT_PATH)
    except IOError:
        print("\n  [FATAL] Could not save output files. Exiting.")
        sys.exit(1)

    # --- Display results ---
    print_sample_readings(all_readings)
    print_summary_per_device(all_readings)

    # --- Final summary ---
    print(f"\n  {'=' * 40}")
    print(f"  SIMULATION COMPLETE")
    print(f"  {'=' * 40}")
    print(f"  CSV  : {CSV_OUTPUT_PATH}")
    print(f"  JSON : {JSON_OUTPUT_PATH}")
    print(f"  Total: {len(all_readings)} records across {len(DEVICE_CONFIGS)} devices")
    if validation_errors == 0:
        print(f"  All readings passed validation")
    else:
        print(f"  WARNING: {validation_errors} validation error(s) found")
    print()


if __name__ == "__main__":
    main()
