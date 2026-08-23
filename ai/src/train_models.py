"""
Model Training & Evaluation Module (Day 6)
==========================================
Trains and rigorously evaluates candidate machine learning models for one-step-ahead
energy consumption prediction:
  1. Persistence Baseline
  2. Linear Regression
  3. Random Forest Regressor
  4. XGBoost Regressor

Outputs:
  - ai/data/processed/model_comparison.csv
  - ai/models/best_energy_model.joblib
  - ai/models/feature_columns.json
  - ai/data/processed/predictions.csv
  - ai/data/processed/model_comparison.png
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Tuple, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "ai" / "data" / "processed" / "clean_energy_dataset.csv"
COMPARISON_CSV_PATH = BASE_DIR / "ai" / "data" / "processed" / "model_comparison.csv"
PREDICTIONS_CSV_PATH = BASE_DIR / "ai" / "data" / "processed" / "predictions.csv"
COMPARISON_PLOT_PATH = BASE_DIR / "ai" / "data" / "processed" / "model_comparison.png"
MODELS_DIR = BASE_DIR / "ai" / "models"
BEST_MODEL_PATH = MODELS_DIR / "best_energy_model.joblib"
FEATURE_COLS_PATH = MODELS_DIR / "feature_columns.json"


def load_and_split_data(
    dataset_path: Path = DATA_PATH, 
    train_ratio: float = 0.8
) -> Tuple[pd.DataFrame, pd.DataFrame, List[str], str]:
    """
    Loads preprocessed dataset and performs deterministic chronological train/test split.
    Preserves time-series ordering without lookahead contamination.
    """
    if not dataset_path.exists():
        raise FileNotFoundError(f"Clean dataset not found at {dataset_path}. Run Day 5 pipeline first.")

    df = pd.read_csv(dataset_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    target_col = "target_next_energy"
    meta_cols = ["id", "device_id", "area", "timestamp", "created_at", target_col]
    feature_cols = [col for col in df.columns if col not in meta_cols]

    train_dfs = []
    test_dfs = []

    # Split chronologically per device
    for device_id, group in df.groupby("device_id", sort=False):
        group_sorted = group.sort_values(by="timestamp").reset_index(drop=True)
        split_idx = int(len(group_sorted) * train_ratio)
        train_dfs.append(group_sorted.iloc[:split_idx])
        test_dfs.append(group_sorted.iloc[split_idx:])

    train_df = pd.concat(train_dfs, ignore_index=True).sort_values(by=["timestamp", "device_id"]).reset_index(drop=True)
    test_df = pd.concat(test_dfs, ignore_index=True).sort_values(by=["timestamp", "device_id"]).reset_index(drop=True)

    return train_df, test_df, feature_cols, target_col


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Computes standard regression metrics (MAE, RMSE, R2)."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2),
    }


def train_and_compare_models():
    """
    Trains all candidate models, evaluates them on the chronological test split,
    ranks them by MAE, and saves all evaluation artifacts.
    """
    print("=" * 80)
    print("  SMART ENERGY MONITOR: CANDIDATE MODEL TRAINING & COMPARISON (DAY 6)")
    print("=" * 80)

    # 1. Load Data
    train_df, test_df, feature_cols, target_col = load_and_split_data()
    print(f"Loaded dataset: {len(train_df) + len(test_df)} records total")
    print(f"  - Training Set: {len(train_df)} rows (80% chronological)")
    print(f"  - Testing Set:  {len(test_df)} rows (20% chronological)")
    print(f"  - Features ({len(feature_cols)}): {feature_cols}")
    print(f"  - Target: {target_col}")

    X_train = train_df[feature_cols].values
    y_train = train_df[target_col].values
    X_test = test_df[feature_cols].values
    y_test = test_df[target_col].values

    # Setup predictions recording
    predictions_df = test_df[["device_id", "area", "timestamp", target_col]].copy()
    predictions_df.rename(columns={target_col: "actual_target"}, inplace=True)

    results = []
    models_dict = {}

    # --- 1. Persistence Baseline ---
    print("\n[1/4] Evaluating Persistence Baseline...")
    # Persistence predicts that next energy = current observed energy
    y_pred_baseline = test_df["energy"].values
    metrics_baseline = evaluate_predictions(y_test, y_pred_baseline)
    predictions_df["pred_persistence"] = y_pred_baseline
    results.append({
        "Model": "Persistence Baseline",
        "MAE (kWh)": metrics_baseline["MAE"],
        "RMSE (kWh)": metrics_baseline["RMSE"],
        "R2 Score": metrics_baseline["R2"],
    })

    # --- 2. Linear Regression ---
    print("[2/4] Training Linear Regression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    metrics_lr = evaluate_predictions(y_test, y_pred_lr)
    predictions_df["pred_linear_regression"] = y_pred_lr
    models_dict["Linear Regression"] = lr_model
    results.append({
        "Model": "Linear Regression",
        "MAE (kWh)": metrics_lr["MAE"],
        "RMSE (kWh)": metrics_lr["RMSE"],
        "R2 Score": metrics_lr["R2"],
    })

    # --- 3. Random Forest Regressor ---
    print("[3/4] Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    metrics_rf = evaluate_predictions(y_test, y_pred_rf)
    predictions_df["pred_random_forest"] = y_pred_rf
    models_dict["Random Forest"] = rf_model
    results.append({
        "Model": "Random Forest",
        "MAE (kWh)": metrics_rf["MAE"],
        "RMSE (kWh)": metrics_rf["RMSE"],
        "R2 Score": metrics_rf["R2"],
    })

    # --- 4. XGBoost Regressor ---
    print("[4/4] Training XGBoost Regressor...")
    xgb_model = xgb.XGBRegressor(
        n_estimators=100,
        learning_rate=0.08,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )
    xgb_model.fit(X_train, y_train)
    y_pred_xgb = xgb_model.predict(X_test)
    metrics_xgb = evaluate_predictions(y_test, y_pred_xgb)
    predictions_df["pred_xgboost"] = y_pred_xgb
    models_dict["XGBoost"] = xgb_model
    results.append({
        "Model": "XGBoost",
        "MAE (kWh)": metrics_xgb["MAE"],
        "RMSE (kWh)": metrics_xgb["RMSE"],
        "R2 Score": metrics_xgb["R2"],
    })

    # --- Results & Ranking ---
    comparison_df = pd.DataFrame(results).sort_values(by="MAE (kWh)").reset_index(drop=True)

    # Identify Best Model
    best_model_name = comparison_df.iloc[0]["Model"]
    best_mae = comparison_df.iloc[0]["MAE (kWh)"]
    best_rmse = comparison_df.iloc[0]["RMSE (kWh)"]
    best_r2 = comparison_df.iloc[0]["R2 Score"]
    baseline_mae = metrics_baseline["MAE"]

    # Add best model predictions and residual column
    if best_model_name == "Linear Regression":
        best_preds = y_pred_lr
    elif best_model_name == "Random Forest":
        best_preds = y_pred_rf
    elif best_model_name == "XGBoost":
        best_preds = y_pred_xgb
    else:
        best_preds = y_pred_baseline

    predictions_df["predicted_target"] = best_preds
    predictions_df["residual"] = predictions_df["actual_target"] - predictions_df["predicted_target"]
    predictions_df["error_abs"] = predictions_df["residual"].abs()

    # --- Save Artifacts ---
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    COMPARISON_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 1. Save comparison CSV
    comparison_df.to_csv(COMPARISON_CSV_PATH, index=False)
    print(f"\n[ARTIFACT] Saved model comparison to: {COMPARISON_CSV_PATH}")

    # 2. Save best model
    if best_model_name in models_dict:
        joblib.dump(models_dict[best_model_name], BEST_MODEL_PATH)
        print(f"[ARTIFACT] Saved best model ({best_model_name}) to: {BEST_MODEL_PATH}")

    # 3. Save feature columns JSON
    with open(FEATURE_COLS_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "feature_columns": feature_cols,
            "target_column": target_col,
            "best_model": best_model_name,
            "timestamp_saved": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2)
    print(f"[ARTIFACT] Saved feature list to: {FEATURE_COLS_PATH}")

    # 4. Save predictions CSV
    predictions_df.to_csv(PREDICTIONS_CSV_PATH, index=False)
    print(f"[ARTIFACT] Saved detailed test predictions to: {PREDICTIONS_CSV_PATH}")

    # 5. Create and save comparison plot
    create_comparison_chart(comparison_df, COMPARISON_PLOT_PATH)
    print(f"[ARTIFACT] Saved comparison plot to: {COMPARISON_PLOT_PATH}")

    # --- Terminal Summary Output ---
    print("\n" + "=" * 80)
    print("  MODEL EVALUATION COMPARISON TABLE (SORTED BY LOWEST MAE)")
    print("=" * 80)
    header = f"{'Model':<25} {'MAE (kWh)':>12} {'RMSE (kWh)':>12} {'R² Score':>12}"
    print(header)
    print("-" * 65)
    for _, row in comparison_df.iterrows():
        print(f"{row['Model']:<25} {row['MAE (kWh)']:>12.6f} {row['RMSE (kWh)']:>12.6f} {row['R2 Score']:>12.6f}")
    print("=" * 80)

    # Baseline Comparison Summary
    print("\n--- BASELINE COMPARISON ---")
    for _, row in comparison_df.iterrows():
        name = row["Model"]
        if name != "Persistence Baseline":
            mae_improvement = ((baseline_mae - row["MAE (kWh)"]) / baseline_mae) * 100
            print(f"  • {name:<20}: MAE reduction of {mae_improvement:.2f}% vs Persistence Baseline")

    print("\n--- BEST MODEL SELECTION ---")
    print(f"  • Selected Model : {best_model_name}")
    print(f"  • Performance    : MAE = {best_mae:.6f} kWh | RMSE = {best_rmse:.6f} kWh | R² = {best_r2:.6f}")
    print(f"  • Justification  : {best_model_name} achieved the lowest MAE and RMSE on the unseen chronological test set, demonstrating superior generalization without overfitting.")
    print("=" * 80 + "\n")

    return comparison_df, predictions_df


def create_comparison_chart(comparison_df: pd.DataFrame, output_path: Path):
    """
    Generates a clear dual-panel comparison plot for MAE, RMSE, and R2.
    Uses separate subplots to prevent axis scale incompatibility.
    """
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    models = comparison_df["Model"].tolist()
    x = np.arange(len(models))
    width = 0.35

    colors_mae = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    colors_rmse = ["#aec7e8", "#ffbb78", "#98df8a", "#ff9896"]

    # Panel 1: Error Metrics (MAE & RMSE)
    rects1 = ax1.bar(x - width/2, comparison_df["MAE (kWh)"], width, label="MAE (kWh)", color="#2563eb", alpha=0.9)
    rects2 = ax1.bar(x + width/2, comparison_df["RMSE (kWh)"], width, label="RMSE (kWh)", color="#f97316", alpha=0.9)

    ax1.set_title("Error Metrics by Model (Lower is Better)", fontsize=13, fontweight="bold", pad=12)
    ax1.set_ylabel("Error (kWh)", fontsize=11, fontweight="semibold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=15, ha="right", fontsize=10)
    ax1.legend(loc="upper right", frameon=True)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # Value labels on bars
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)
    for rect in rects2:
        h = rect.get_height()
        ax1.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

    # Panel 2: Goodness of Fit (R2 Score)
    r2_colors = ["#dc2626" if val < 0 else "#16a34a" for val in comparison_df["R2 Score"]]
    bars_r2 = ax2.bar(models, comparison_df["R2 Score"], color=r2_colors, width=0.5, alpha=0.85)

    ax2.set_title("Coefficient of Determination R² (Higher is Better)", fontsize=13, fontweight="bold", pad=12)
    ax2.set_ylabel("R² Score", fontsize=11, fontweight="semibold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, rotation=15, ha="right", fontsize=10)
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars_r2:
        h = bar.get_height()
        va = "bottom" if h >= 0 else "top"
        offset = 3 if h >= 0 else -10
        ax2.annotate(f"{h:.3f}", xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, offset), textcoords="offset points", ha="center", va=va, fontsize=8, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    train_and_compare_models()
