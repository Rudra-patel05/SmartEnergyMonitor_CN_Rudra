"""
Feature Engineering & Dataset Preparation Module
================================================
Constructs temporal, electrical, environmental, lag, and rolling features.
Defines the prediction target without lookahead data leakage.
Performs chronological train/test splitting and evaluates a persistent baseline predictor.
Outputs the final ML-ready dataset to ai/data/processed/clean_energy_dataset.csv.
"""

import os
import sys
from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Ensure sibling imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load_data import load_raw_data_from_db
from clean_data import clean_energy_data

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_CSV_PATH = BASE_DIR / "ai" / "data" / "processed" / "clean_energy_dataset.csv"


def create_features_and_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates engineered features and defines the forecasting target per device.

    Features Created:
      - Temporal: hour, minute, day_of_week, is_weekend
      - Sensor/State: occupancy, temperature, voltage, current, power
      - Lag/Historical:
          - previous_energy (lag 1)
          - previous_power (lag 1)
          - energy_rolling_mean_3 (rolling 3-step mean)
          - power_rolling_mean_3 (rolling 3-step mean)
          - energy_delta (incremental consumption from previous step)
      - Target:
          - target_next_energy: Next observed energy value (t+1) for the same device

    Ensures zero lookahead data leakage (features only use past/present information).
    """
    # Work on sorted copy
    df_feat = df.copy()
    df_feat["timestamp"] = pd.to_datetime(df_feat["timestamp"])
    df_feat = df_feat.sort_values(by=["device_id", "timestamp"]).reset_index(drop=True)

    # 1. Temporal Features
    df_feat["hour"] = df_feat["timestamp"].dt.hour
    df_feat["minute"] = df_feat["timestamp"].dt.minute
    df_feat["day_of_week"] = df_feat["timestamp"].dt.dayofweek
    df_feat["is_weekend"] = df_feat["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

    # Group by device to avoid cross-device lag contamination
    grouped = df_feat.groupby("device_id")

    # 2. Lag Features (Historical, NO leakage)
    df_feat["previous_energy"] = grouped["energy"].shift(1)
    df_feat["previous_power"] = grouped["power"].shift(1)

    # 3. Rolling Window Features (min_periods=1 to preserve points, closed='left' logic via shift)
    # Rolling 3-step energy and power using prior observations
    df_feat["energy_rolling_mean_3"] = (
        grouped["energy"]
        .transform(lambda x: x.shift(1).rolling(window=3, min_periods=1).mean())
    )
    df_feat["power_rolling_mean_3"] = (
        grouped["power"]
        .transform(lambda x: x.shift(1).rolling(window=3, min_periods=1).mean())
    )

    # Fill initial lag NaN with first observed values to prevent data loss
    df_feat["previous_energy"] = df_feat["previous_energy"].fillna(df_feat["energy"])
    df_feat["previous_power"] = df_feat["previous_power"].fillna(df_feat["power"])
    df_feat["energy_rolling_mean_3"] = df_feat["energy_rolling_mean_3"].fillna(df_feat["energy"])
    df_feat["power_rolling_mean_3"] = df_feat["power_rolling_mean_3"].fillna(df_feat["power"])

    # 4. Incremental Energy Delta
    df_feat["energy_delta"] = (df_feat["energy"] - df_feat["previous_energy"]).clip(lower=0.0)

    # 5. Define Target Variable: Next Step Energy (t+1) for the same device
    df_feat["target_next_energy"] = grouped["energy"].shift(-1)

    # Drop the last record per device because future target (t+1) is not observed
    initial_len = len(df_feat)
    df_feat = df_feat.dropna(subset=["target_next_energy"]).reset_index(drop=True)
    dropped_target_na = initial_len - len(df_feat)
    print(f"[FEATURE ENG] Created features. Dropped {dropped_target_na} terminal records with unobserved future targets.")

    return df_feat


def chronological_split(
    df: pd.DataFrame, 
    train_ratio: float = 0.8
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits time-series dataset chronologically (e.g. 80% train, 20% test).
    Splits per device to maintain balanced device representation across time.
    """
    train_dfs = []
    test_dfs = []

    for device_id, group in df.groupby("device_id", sort=False):
        group_sorted = group.sort_values(by="timestamp").reset_index(drop=True)
        split_idx = int(len(group_sorted) * train_ratio)
        train_dfs.append(group_sorted.iloc[:split_idx])
        test_dfs.append(group_sorted.iloc[split_idx:])

    train_df = pd.concat(train_dfs, ignore_index=True).sort_values(by=["timestamp", "device_id"]).reset_index(drop=True)
    test_df = pd.concat(test_dfs, ignore_index=True).sort_values(by=["timestamp", "device_id"]).reset_index(drop=True)

    return train_df, test_df


def evaluate_baseline_predictor(
    train_df: pd.DataFrame, 
    test_df: pd.DataFrame, 
    target_col: str = "target_next_energy"
) -> Dict[str, float]:
    """
    Evaluates a persistence / naive baseline predictor:
    Prediction y_hat(t+1) = y(t) (the current observed energy value).
    """
    y_test_true = test_df[target_col].values
    y_test_pred_baseline = test_df["energy"].values  # persistent baseline

    mae = mean_absolute_error(y_test_true, y_test_pred_baseline)
    rmse = np.sqrt(mean_squared_error(y_test_true, y_test_pred_baseline))
    r2 = r2_score(y_test_true, y_test_pred_baseline)
    
    # Calculate Mean Absolute Percentage Error (avoiding zero division)
    non_zero_mask = y_test_true > 0
    mape = np.mean(np.abs((y_test_true[non_zero_mask] - y_test_pred_baseline[non_zero_mask]) / y_test_true[non_zero_mask])) * 100

    metrics = {
        "Baseline Strategy": "Persistence Model (Predict Next Energy = Current Energy)",
        "MAE (kWh)": float(mae),
        "RMSE (kWh)": float(rmse),
        "R2 Score": float(r2),
        "MAPE (%)": float(mape),
    }
    return metrics


def run_pipeline() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Executes the end-to-end Day 5 Data Preprocessing Pipeline.
    """
    print("=" * 80)
    print("  SMART ENERGY MONITOR: ML DATA PREPARATION PIPELINE (DAY 5)")
    print("=" * 80)

    # 1. Load Data
    raw_df = load_raw_data_from_db()
    print(f"Step 1: Loaded {len(raw_df)} raw records from SQLite database.")

    # 2. Clean Data & Exclude Test Records
    cleaned_df, excluded_test_df = clean_energy_data(raw_df)
    print(f"Step 2: Cleaned data. Excluded {len(excluded_test_df)} test records. Clean row count: {len(cleaned_df)}.")

    # 3. Feature Engineering & Target Construction
    ml_df = create_features_and_target(cleaned_df)
    print(f"Step 3: Engineered temporal, sensor, lag, and rolling features. Valid dataset rows: {len(ml_df)}.")

    # 4. Save Clean Processed Dataset
    PROCESSED_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ml_df.to_csv(PROCESSED_CSV_PATH, index=False)
    print(f"Step 4: Saved processed dataset to: {PROCESSED_CSV_PATH}")

    # 5. Chronological Train/Test Split
    train_df, test_df = chronological_split(ml_df, train_ratio=0.8)
    print(f"Step 5: Chronological Train/Test Split (80/20):")
    print(f"        - Training records: {len(train_df)} (80%)")
    print(f"        - Testing records:  {len(test_df)} (20%)")

    # 6. Baseline Evaluation
    baseline_metrics = evaluate_baseline_predictor(train_df, test_df)
    print("\nStep 6: Baseline Model Evaluation (Persistence Benchmark):")
    for k, v in baseline_metrics.items():
        if isinstance(v, float):
            print(f"        - {k:<20}: {v:.6f}")
        else:
            print(f"        - {k:<20}: {v}")

    # Feature List
    feature_cols = [
        col for col in ml_df.columns 
        if col not in ["id", "device_id", "area", "timestamp", "created_at", "target_next_energy"]
    ]

    print("\n" + "=" * 80)
    print("  VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Final Dataset Row Count: {len(ml_df)}")
    print(f"Feature Names ({len(feature_cols)} features): {feature_cols}")
    print(f"Target Name:             target_next_energy")
    print(f"Train Rows:              {len(train_df)}")
    print(f"Test Rows:               {len(test_df)}")
    print("\nFirst 5 Processed Rows (Selected Columns):")
    sample_cols = ["device_id", "timestamp", "voltage", "current", "power", "energy", "previous_energy", "target_next_energy"]
    print(ml_df[sample_cols].head(5).to_string(index=False))
    print("=" * 80 + "\n")

    return ml_df, train_df, test_df


if __name__ == "__main__":
    run_pipeline()
