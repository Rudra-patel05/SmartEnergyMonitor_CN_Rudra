import os
import sys
from pathlib import Path
from typing import Tuple, Dict, Any, List, Optional
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Setup Paths to the clean AI data
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CLEAN_DATA_PATH = BASE_DIR / "ai" / "data" / "processed" / "clean_energy_dataset.csv"

# Same features from ai/src/anomaly_detection.py
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

class AnomalyDetectionService:
    def __init__(self):
        self.model: Optional[IsolationForest] = None
        self.is_ready = False
        
        # We will attempt to train the model on initialization
        self._initialize_model()
        
    def _initialize_model(self):
        """Loads clean data and trains the IsolationForest model to match Day 7 exactly."""
        try:
            if not CLEAN_DATA_PATH.exists():
                print(f"[AnomalyService] Clean dataset not found at {CLEAN_DATA_PATH}")
                return
                
            clean_df = pd.read_csv(CLEAN_DATA_PATH)
            
            # Train using the exact same parameters as anomaly_detection.py
            self.model = IsolationForest(
                n_estimators=150,
                max_samples="auto",
                contamination=0.04,
                random_state=42,
                n_jobs=-1
            )
            
            X_train = clean_df[ANOMALY_FEATURES].values
            self.model.fit(X_train)
            self.is_ready = True
            print(f"[AnomalyService] Successfully initialized IsolationForest model with {len(clean_df)} records.")
            
        except Exception as e:
            print(f"[AnomalyService] Failed to initialize model: {e}")

    def check_anomaly(self, features: Dict[str, Any]) -> Tuple[int, float]:
        """
        Takes a feature dictionary containing exactly the keys in ANOMALY_FEATURES
        Returns (anomaly_flag, anomaly_score)
        """
        if not self.is_ready or self.model is None:
            raise RuntimeError("Anomaly Detection model is not initialized.")
            
        # Ensure correct order
        feature_values = []
        for feat in ANOMALY_FEATURES:
            if feat not in features:
                raise ValueError(f"Missing required feature: {feat}")
            feature_values.append(features[feat])
            
        X = np.array([feature_values])
        
        # -1 = anomaly, 1 = normal
        raw_pred = self.model.predict(X)[0]
        score = float(self.model.decision_function(X)[0])
        
        anomaly_flag = 1 if raw_pred == -1 else 0
        
        return anomaly_flag, score
        
    def calculate_features(self, current_reading: Dict[str, Any], history_readings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates the derived features (hour, energy_delta, power_rolling_mean_3)
        current_reading: Dict from AnomalyCheckRequest
        history_readings: List of dicts representing the most recent 2 previous readings for the same device
                          Sorted descending by time (index 0 is the most recent previous reading)
        """
        timestamp_str = current_reading["timestamp"]
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        hour = dt.hour
        
        power = current_reading["power"]
        energy = current_reading["energy"]
        
        if len(history_readings) == 0:
            energy_delta = 0.0
            power_rolling_mean_3 = power
        else:
            prev_energy = history_readings[0]["energy"]
            energy_delta = max(0.0, energy - prev_energy)
            
            # power_rolling_mean_3 uses the previous 3 readings for the rolling mean (or fewer if not available)
            # wait, in feature_engineering:
            # df_feat["power_rolling_mean_3"] = grouped["power"].transform(lambda x: x.shift(1).rolling(window=3, min_periods=1).mean())
            # This means power_rolling_mean_3 AT time t is the mean of power at t-1, t-2, t-3.
            past_powers = [r["power"] for r in history_readings[:3]]
            if len(past_powers) > 0:
                power_rolling_mean_3 = sum(past_powers) / len(past_powers)
            else:
                power_rolling_mean_3 = power
                
        features = {
            "power": power,
            "current": current_reading["current"],
            "voltage": current_reading["voltage"],
            "temperature": current_reading["temperature"],
            "occupancy": current_reading["occupancy"],
            "hour": hour,
            "energy_delta": energy_delta,
            "power_rolling_mean_3": power_rolling_mean_3
        }
        
        return features

# Global instance
anomaly_service = AnomalyDetectionService()
