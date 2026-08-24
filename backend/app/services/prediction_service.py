"""
prediction_service.py — Day 9
================================
Singleton service that loads the pre-trained XGBoost model once and exposes
helper functions for on-request energy prediction.

Architecture notes
------------------
* The model is loaded **once** at module import time (module-level singleton).
  FastAPI workers reuse the same loaded object — no per-request I/O.
* Features are derived entirely from **historical readings already stored in
  SQLite**. No future information is used.
* If a device has fewer than 3 readings in the database the service raises an
  HTTPException(422) because the rolling-mean features cannot be computed.
* Predictions are computed on request and NOT stored in the database, so the
  Day 8 SQLite schema is untouched.

Feature derivation table
-------------------------
Feature                  | Source
------------------------ | --------------------------------------------------
voltage                  | Latest reading from DB
current                  | Latest reading from DB
power                    | Latest reading from DB
energy                   | Latest reading from DB
temperature              | Latest reading from DB
occupancy                | Latest reading from DB
hour                     | Parsed from latest reading timestamp (datetime.hour)
minute                   | Parsed from latest reading timestamp (datetime.minute)
day_of_week              | Parsed from latest reading timestamp (0=Mon…6=Sun)
is_weekend               | 1 if day_of_week >= 5 else 0
previous_energy          | energy of reading N-1 (second-latest)
previous_power           | power  of reading N-1 (second-latest)
energy_rolling_mean_3    | mean(energy) over last 3 readings (N, N-1, N-2)
power_rolling_mean_3     | mean(power)  over last 3 readings (N, N-1, N-2)
energy_delta             | energy[N] − energy[N-1]
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import EnergyReading

# ---------------------------------------------------------------------------
# Paths — resolved relative to this file so they work regardless of CWD
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
_AI_MODELS_DIR = os.path.join(_PROJECT_ROOT, "ai", "models")

_MODEL_PATH = os.path.join(_AI_MODELS_DIR, "best_energy_model.joblib")
_FEATURE_META_PATH = os.path.join(_AI_MODELS_DIR, "feature_columns.json")

# ---------------------------------------------------------------------------
# Module-level singleton: loaded once, reused for every request
# ---------------------------------------------------------------------------
_model: Any = None
_feature_columns: List[str] = []
_model_name: str = "XGBoost"
_load_error: str = ""


def _load_model() -> None:
    """Load model and feature metadata from disk. Called once at import time."""
    global _model, _feature_columns, _model_name, _load_error

    # --- Load feature metadata ---
    if not os.path.isfile(_FEATURE_META_PATH):
        _load_error = f"Feature metadata not found at: {_FEATURE_META_PATH}"
        return

    with open(_FEATURE_META_PATH, "r") as f:
        meta = json.load(f)

    _feature_columns = meta.get("feature_columns", [])
    _model_name = meta.get("best_model", "XGBoost")

    if not _feature_columns:
        _load_error = "feature_columns list is empty in feature_columns.json"
        return

    # --- Load model ---
    if not os.path.isfile(_MODEL_PATH):
        _load_error = f"Model file not found at: {_MODEL_PATH}"
        return

    try:
        _model = joblib.load(_MODEL_PATH)
        _load_error = ""
    except Exception as exc:  # noqa: BLE001
        _load_error = f"Failed to load model: {exc}"


# Load immediately on import
_load_model()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _assert_model_ready() -> None:
    """Raise 503 if the model failed to load."""
    if _load_error or _model is None:
        raise HTTPException(
            status_code=503,
            detail=f"Prediction service unavailable: {_load_error or 'model not loaded'}",
        )


def _get_device_readings(device_id: str, db: Session, n: int = 3) -> List[EnergyReading]:
    """
    Return the last *n* readings for *device_id*, ordered oldest-first.
    Raises 404 if the device has no readings, 422 if fewer than *n* exist.
    """
    rows = (
        db.query(EnergyReading)
        .filter(EnergyReading.device_id == device_id)
        .order_by(EnergyReading.timestamp.desc())
        .limit(n)
        .all()
    )

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"Device '{device_id}' not found — no readings in database.",
        )

    if len(rows) < n:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Device '{device_id}' has only {len(rows)} reading(s). "
                f"A minimum of {n} readings are required to compute rolling-mean "
                "lag features. Please wait for more data to accumulate."
            ),
        )

    # Reverse so index 0 = oldest, index -1 = latest
    return list(reversed(rows))


def _build_feature_row(readings: List[EnergyReading]) -> pd.DataFrame:
    """
    Derive all 15 model features from a list of ≥3 readings.

    Parameters
    ----------
    readings : list[EnergyReading]
        Ordered oldest → latest. Must contain at least 3 entries.

    Returns
    -------
    pd.DataFrame with a single row, columns matching ``_feature_columns``.
    """
    latest = readings[-1]   # index N (current)
    prev   = readings[-2]   # index N-1

    # --- Parse timestamp from latest reading ---
    # Stored format: "YYYY-MM-DD HH:MM:SS"
    try:
        ts = datetime.strptime(latest.timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # Fall back gracefully if format differs
        ts = datetime.utcnow()

    hour        = ts.hour
    minute      = ts.minute
    day_of_week = ts.weekday()            # 0 = Monday, 6 = Sunday
    is_weekend  = 1 if day_of_week >= 5 else 0

    # --- Lag features ---
    previous_energy = prev.energy
    previous_power  = prev.power

    energies = [r.energy for r in readings]
    powers   = [r.power  for r in readings]

    energy_rolling_mean_3 = float(np.mean(energies))
    power_rolling_mean_3  = float(np.mean(powers))
    energy_delta          = latest.energy - prev.energy

    row = {
        "voltage":               latest.voltage,
        "current":               latest.current,
        "power":                 latest.power,
        "energy":                latest.energy,
        "temperature":           latest.temperature,
        "occupancy":             latest.occupancy,
        "hour":                  hour,
        "minute":                minute,
        "day_of_week":           day_of_week,
        "is_weekend":            is_weekend,
        "previous_energy":       previous_energy,
        "previous_power":        previous_power,
        "energy_rolling_mean_3": energy_rolling_mean_3,
        "power_rolling_mean_3":  power_rolling_mean_3,
        "energy_delta":          energy_delta,
    }

    # Build DataFrame with features in the exact order the model expects
    df = pd.DataFrame([row])[_feature_columns]
    return df


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def predict_next_energy(device_id: str, db: Session) -> Dict[str, Any]:
    """
    Predict the next energy reading for *device_id*.

    Queries the last 3 readings from the database, derives all 15 model
    features, runs inference, and returns a prediction dict.

    Returns
    -------
    dict with keys: device_id, area, timestamp, predicted_next_energy, model_name
    """
    _assert_model_ready()

    readings = _get_device_readings(device_id, db, n=3)
    latest   = readings[-1]

    feature_df = _build_feature_row(readings)

    # Run inference (XGBoost via sklearn wrapper → returns ndarray)
    pred_array = _model.predict(feature_df)
    predicted_value = float(pred_array[0])
    # Clamp to non-negative (energy can't be negative)
    predicted_value = max(0.0, round(predicted_value, 6))

    return {
        "device_id":              device_id,
        "area":                   latest.area,
        "timestamp":              datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "predicted_next_energy":  predicted_value,
        "model_name":             _model_name,
    }


def get_latest_predictions(db: Session) -> List[Dict[str, Any]]:
    """
    Return a prediction for every distinct device currently in the database.

    Devices with fewer than 3 readings are skipped (with an error note), so
    this endpoint never fails entirely when some devices lack history.

    Returns
    -------
    list of dicts — each element is either a prediction dict (status='ok') or
    an error dict (status='error') for devices that could not be predicted.
    """
    _assert_model_ready()

    # Get all distinct device IDs
    device_rows = (
        db.query(EnergyReading.device_id)
        .distinct()
        .all()
    )
    device_ids = [row[0] for row in device_rows]

    results = []
    for device_id in device_ids:
        try:
            pred = predict_next_energy(device_id, db)
            pred["status"] = "ok"
            results.append(pred)
        except HTTPException as exc:
            results.append({
                "device_id":  device_id,
                "status":     "error",
                "detail":     exc.detail,
            })

    return results
