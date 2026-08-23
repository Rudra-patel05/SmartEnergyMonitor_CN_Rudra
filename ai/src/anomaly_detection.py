"""
Anomaly Detection Module (Day 7)
================================
Implements unsupervised anomaly detection for campus energy telemetry using Isolation Forest.
Constructs a dedicated synthetic anomaly test set with realistic physical fault scenarios,
evaluates precision/recall/F1/FPR metrics, and exports visual and CSV audit artifacts.

Outputs:
  - ai/data/anomaly/synthetic_anomalies.csv
  - ai/data/anomaly/anomaly_predictions.csv
  - ai/data/anomaly/anomaly_metrics.csv
  - ai/data/anomaly/anomaly_distribution.png
"""

import os
import sys
import json
from pathlib import Path
from typing import Tuple, Dict, Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CLEAN_DATA_PATH = BASE_DIR / "ai" / "data" / "processed" / "clean_energy_dataset.csv"
ANOMALY_DIR = BASE_DIR / "ai" / "data" / "anomaly"

SYNTHETIC_DATA_PATH = ANOMALY_DIR / "synthetic_anomalies.csv"
PREDICTIONS_PATH = ANOMALY_DIR / "anomaly_predictions.csv"
METRICS_PATH = ANOMALY_DIR / "anomaly_metrics.csv"
CHART_PATH = ANOMALY_DIR / "anomaly_distribution.png"

# Selected features for anomaly detection
ANOMALY_FEATURES = [
    "power",
    "current",
    "voltage",
    "temperature",
    "occupancy",
    "hour",
    "energy_delta",
    "power_rolling_mean_3",
]


def load_clean_data(filepath: Path = CLEAN_DATA_PATH) -> pd.DataFrame:
    """Loads the clean energy dataset without modifying it."""
    if not filepath.exists():
        raise FileNotFoundError(f"Clean energy dataset not found at {filepath}")
    return pd.read_csv(filepath)


def generate_synthetic_anomaly_dataset(
    clean_df: pd.DataFrame, 
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Creates a separate labeled evaluation dataset containing:
      - All unmodified clean records (labeled as normal, is_synthetic_anomaly = 0).
      - Injected realistic synthetic anomalies (labeled as abnormal, is_synthetic_anomaly = 1).

    Simulated Scenarios:
      1. Sudden Power/Current Surge (Equipment malfunction or short overload).
      2. Off-Hours High Consumption (HVAC or lab computers left active overnight with 0 occupancy).
      3. Severe Voltage Sag/Surge with abnormal current (Grid instability).
      4. Abnormal Energy Delta Surge with zero occupancy.
    """
    np.random.seed(random_seed)
    df_eval = clean_df.copy()
    df_eval["is_synthetic_anomaly"] = 0
    df_eval["anomaly_type"] = "normal"

    # Select random indices to clone and perturb for synthetic anomalies
    # Inverting ~4% (24 records across 5 devices)
    num_anomalies = 24
    sample_indices = np.random.choice(df_eval.index, size=num_anomalies, replace=False)
    
    anomalous_rows = []
    
    # Split into 4 scenarios (6 records each)
    scenarios = [
        ("power_spike", sample_indices[0:6]),
        ("off_hours_high_load", sample_indices[6:12]),
        ("voltage_anomaly", sample_indices[12:18]),
        ("energy_delta_surge", sample_indices[18:24]),
    ]

    for scenario_name, idx_list in scenarios:
        for idx in idx_list:
            row = clean_df.loc[idx].copy()
            row["is_synthetic_anomaly"] = 1
            row["anomaly_type"] = scenario_name

            if scenario_name == "power_spike":
                # Spike power by 3.5x-4.5x and current accordingly
                multiplier = np.random.uniform(3.5, 4.8)
                row["power"] = round(row["power"] * multiplier, 2)
                row["current"] = round(row["power"] / row["voltage"], 2)
                row["energy_delta"] = round(row["energy_delta"] * multiplier, 4)

            elif scenario_name == "off_hours_high_load":
                # Force off-hours (01:00-04:00), zero occupancy, high power (1800W-2500W)
                row["hour"] = np.random.choice([1, 2, 3, 4])
                row["occupancy"] = 0
                row["power"] = round(np.random.uniform(1800.0, 2500.0), 2)
                row["current"] = round(row["power"] / row["voltage"], 2)
                row["energy_delta"] = round(np.random.uniform(0.45, 0.75), 4)

            elif scenario_name == "voltage_anomaly":
                # Severe voltage drop (175V-185V) or overvoltage (270V-285V)
                row["voltage"] = np.random.choice([
                    np.random.uniform(175.0, 185.0),
                    np.random.uniform(270.0, 285.0)
                ])
                row["voltage"] = round(row["voltage"], 1)
                row["current"] = round(np.random.uniform(8.0, 12.5), 2)
                row["power"] = round(row["voltage"] * row["current"], 2)

            elif scenario_name == "energy_delta_surge":
                # Step energy consumption 10x normal rate with 0 occupants
                row["occupancy"] = 0
                row["energy_delta"] = round(row["energy_delta"] * 10.0 + 0.5, 4)
                row["power"] = round(np.random.uniform(1500.0, 2200.0), 2)
                row["current"] = round(row["power"] / row["voltage"], 2)

            anomalous_rows.append(row)

    # Combine clean records with synthetic anomaly rows
    df_synthetic = pd.concat([df_eval, pd.DataFrame(anomalous_rows)], ignore_index=True)
    df_synthetic = df_synthetic.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    return df_synthetic


def train_isolation_forest(
    clean_df: pd.DataFrame,
    features: List[str] = ANOMALY_FEATURES,
    contamination: float = 0.04,
    random_state: int = 42
) -> IsolationForest:
    """
    Trains an Isolation Forest model exclusively on the clean baseline telemetry data.
    """
    X_train = clean_df[features].values
    model = IsolationForest(
        n_estimators=150,
        max_samples="auto",
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(X_train)
    return model


def evaluate_anomaly_detection(
    model: IsolationForest,
    eval_df: pd.DataFrame,
    features: List[str] = ANOMALY_FEATURES
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Applies the Isolation Forest model to the evaluation dataset and calculates
    precision, recall, F1-score, and False Positive Rate.
    """
    X_eval = eval_df[features].values

    # Isolation forest outputs -1 for anomaly and 1 for normal
    raw_preds = model.predict(X_eval)
    # Decision function: lower values mean more abnormal
    scores = model.decision_function(X_eval)

    results_df = eval_df.copy()
    results_df["anomaly_score"] = scores
    # Convert to binary: 1 = anomaly, 0 = normal
    results_df["predicted_anomaly"] = np.where(raw_preds == -1, 1, 0)

    y_true = results_df["is_synthetic_anomaly"].values
    y_pred = results_df["predicted_anomaly"].values

    # Confusion matrix & metrics
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    metrics = {
        "Total Evaluation Records": len(eval_df),
        "Normal Records (Ground Truth)": int(tn + fp),
        "Synthetic Anomalies (Ground Truth)": int(tp + fn),
        "Detected Anomalies (Total)": int(tp + fp),
        "Detected Normal (Total)": int(tn + fn),
        "True Positives (TP)": int(tp),
        "False Positives (FP)": int(fp),
        "True Negatives (TN)": int(tn),
        "False Negatives (FN)": int(fn),
        "Precision": float(precision),
        "Recall": float(recall),
        "F1-Score": float(f1),
        "False Positive Rate (FPR)": float(fpr),
        "Model Contamination Parameter": float(model.contamination),
    }

    return results_df, metrics


def create_anomaly_visualization(
    results_df: pd.DataFrame,
    metrics: Dict[str, Any],
    output_path: Path = CHART_PATH
):
    """
    Generates a dual-panel visualization:
      Panel 1: Ground truth vs model prediction count comparison.
      Panel 2: Anomaly score distribution by class.
    """
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=300)

    # Panel 1: Bar counts
    labels = ["Normal Records", "Anomalous Records"]
    actual_counts = [metrics["Normal Records (Ground Truth)"], metrics["Synthetic Anomalies (Ground Truth)"]]
    pred_counts = [metrics["Detected Normal (Total)"], metrics["Detected Anomalies (Total)"]]

    x = np.arange(len(labels))
    width = 0.35

    rects1 = ax1.bar(x - width/2, actual_counts, width, label="Ground Truth", color="#2563eb", alpha=0.9)
    rects2 = ax1.bar(x + width/2, pred_counts, width, label="Model Predictions", color="#f97316", alpha=0.9)

    ax1.set_title("Ground Truth vs. Predicted Anomaly Counts", fontsize=12, fontweight="bold", pad=12)
    ax1.set_ylabel("Number of Records", fontsize=11, fontweight="semibold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=10, fontweight="medium")
    ax1.legend(loc="upper right", frameon=True)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f"{h}", xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")
    for rect in rects2:
        h = rect.get_height()
        ax1.annotate(f"{h}", xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

    # Panel 2: Anomaly Score Distribution
    normal_scores = results_df[results_df["is_synthetic_anomaly"] == 0]["anomaly_score"]
    anomaly_scores = results_df[results_df["is_synthetic_anomaly"] == 1]["anomaly_score"]

    ax2.hist(normal_scores, bins=30, alpha=0.65, label="Normal Records (GT=0)", color="#10b981", edgecolor="black")
    ax2.hist(anomaly_scores, bins=15, alpha=0.85, label="Synthetic Anomalies (GT=1)", color="#ef4444", edgecolor="black")

    ax2.axvline(0, color="black", linestyle="--", linewidth=1.2, label="Anomaly Threshold (Score = 0)")
    ax2.set_title("Isolation Forest Anomaly Score Distribution", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("Anomaly Score (Lower / Negative = Anomalous)", fontsize=11, fontweight="semibold")
    ax2.set_ylabel("Frequency", fontsize=11, fontweight="semibold")
    ax2.legend(loc="upper left", frameon=True)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


def run_anomaly_pipeline():
    """Executes the full Day 7 Anomaly Detection pipeline."""
    print("=" * 80)
    print("  SMART ENERGY MONITOR: ANOMALY DETECTION PIPELINE (DAY 7)")
    print("=" * 80)

    # 1. Load clean dataset
    clean_df = load_clean_data()
    print(f"Step 1: Loaded clean dataset: {len(clean_df)} records")
    print(f"        Features selected ({len(ANOMALY_FEATURES)}): {ANOMALY_FEATURES}")

    # 2. Train Isolation Forest
    contamination = 0.04
    print(f"\nStep 2: Training Isolation Forest (contamination={contamination}, n_estimators=150)...")
    model = train_isolation_forest(clean_df, features=ANOMALY_FEATURES, contamination=contamination)
    print("        Model trained successfully on baseline telemetry.")

    # 3. Create synthetic anomaly evaluation dataset
    print("\nStep 3: Generating synthetic anomaly test dataset...")
    synthetic_df = generate_synthetic_anomaly_dataset(clean_df, random_seed=42)
    num_synthetic = (synthetic_df["is_synthetic_anomaly"] == 1).sum()
    num_normal = (synthetic_df["is_synthetic_anomaly"] == 0).sum()
    print(f"        Total evaluation rows: {len(synthetic_df)} ({num_normal} normal + {num_synthetic} synthetic anomalies)")

    # 4. Evaluate Detection
    print("\nStep 4: Evaluating detection performance...")
    results_df, metrics = evaluate_anomaly_detection(model, synthetic_df, features=ANOMALY_FEATURES)

    # 5. Save Artifacts
    ANOMALY_DIR.mkdir(parents=True, exist_ok=True)
    synthetic_df.to_csv(SYNTHETIC_DATA_PATH, index=False)
    results_df.to_csv(PREDICTIONS_PATH, index=False)

    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(METRICS_PATH, index=False)

    create_anomaly_visualization(results_df, metrics, CHART_PATH)

    print("\n" + "=" * 80)
    print("  ANOMALY DETECTION EVALUATION RESULTS (SYNTHETIC BENCHMARK)")
    print("=" * 80)
    for k, v in metrics.items():
        if isinstance(v, float):
            print(f"  • {k:<38}: {v:.6f}")
        else:
            print(f"  • {k:<38}: {v}")
    print("=" * 80)

    print(f"\n[ARTIFACTS SAVED]")
    print(f"  1. Synthetic Dataset   : {SYNTHETIC_DATA_PATH}")
    print(f"  2. Anomaly Predictions : {PREDICTIONS_PATH}")
    print(f"  3. Anomaly Metrics     : {METRICS_PATH}")
    print(f"  4. Distribution Chart  : {CHART_PATH}\n")

    return results_df, metrics


if __name__ == "__main__":
    run_anomaly_pipeline()
