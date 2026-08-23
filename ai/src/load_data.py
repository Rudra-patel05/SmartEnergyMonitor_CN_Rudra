"""
Load Data Module
================
Reads raw energy readings from the SQLite database (backend/energy.db)
and saves an unmodified snapshot into ai/data/raw/raw_energy_readings.csv.
"""

import os
import sqlite3
from pathlib import Path
import pandas as pd

# Default paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "backend" / "energy.db"
DEFAULT_RAW_CSV_PATH = BASE_DIR / "ai" / "data" / "raw" / "raw_energy_readings.csv"


def get_db_connection(db_path=None):
    """
    Establish a connection to the SQLite database.
    """
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    if not path.exists():
        raise FileNotFoundError(f"Database not found at {path}")
    return sqlite3.connect(path)


def load_raw_data_from_db(db_path=None, save_raw_csv=True, raw_csv_path=None) -> pd.DataFrame:
    """
    Loads all records from the energy_readings table in SQLite.

    Args:
        db_path: Path to SQLite database file.
        save_raw_csv: If True, saves an unmodified copy to raw data folder.
        raw_csv_path: Destination path for raw CSV snapshot.

    Returns:
        pd.DataFrame containing all raw records.
    """
    conn = get_db_connection(db_path)
    query = """
    SELECT 
        id,
        device_id,
        area,
        timestamp,
        voltage,
        current,
        power,
        energy,
        temperature,
        occupancy,
        created_at
    FROM energy_readings
    ORDER BY id ASC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if save_raw_csv:
        csv_dest = Path(raw_csv_path) if raw_csv_path else DEFAULT_RAW_CSV_PATH
        csv_dest.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_dest, index=False)
        print(f"[LOAD] Raw snapshot saved to: {csv_dest} ({len(df)} records)")

    return df


if __name__ == "__main__":
    print("=" * 60)
    print("  AI DATA LOADER: Loading Raw Energy Readings")
    print("=" * 60)
    df_raw = load_raw_data_from_db()
    print(f"Total raw records loaded: {len(df_raw)}")
    print(f"Columns: {list(df_raw.columns)}")
    print("\nFirst 3 rows:")
    print(df_raw.head(3))
    print("\nLast 3 rows:")
    print(df_raw.tail(3))
