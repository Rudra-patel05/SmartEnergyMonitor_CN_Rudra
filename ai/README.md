# AI / Machine Learning Module – SmartEnergyMonitor

> Smart Energy Monitor – Smart Campus (GTU PBL)  
> Module: `ai/` – Telemetry Preprocessing, Feature Engineering, Energy Prediction, and Unsupervised Anomaly Detection.

---

## 1. Overview & Objectives

The `ai/` module provides end-to-end intelligence for the Smart Campus Energy Monitoring platform:
1. **Data Ingestion & Cleaning (Day 5)**: SQLite reading ingestion, quality checks, test fixture exclusion, 15 engineered features, zero-leakage target, and chronological 80/20 train/test split.
2. **Energy Consumption Forecasting (Day 6)**: Candidate model training (Linear Regression, Random Forest, XGBoost, Persistence) for one-step-ahead prediction ($E_{t+1}$).
3. **Unsupervised Anomaly Detection (Day 7)**: Isolation Forest training for detecting power surges, off-hours wastage, and grid instabilities.

---

## 2. Directory Structure

```
ai/
├── data/
│   ├── raw/
│   │   └── raw_energy_readings.csv        # Immutable snapshot of raw SQLite table (614 rows)
│   ├── processed/
│   │   ├── clean_energy_dataset.csv       # ML-ready engineered dataset (605 rows)
│   │   ├── model_comparison.csv           # Model evaluation results sorted by MAE
│   │   ├── model_comparison.png           # Dual-panel comparative visualization
│   │   └── predictions.csv                # Per-record actuals, predictions, and residuals
│   └── anomaly/
│       ├── synthetic_anomalies.csv        # Labeled evaluation dataset (normal + synthetic faults)
│       ├── anomaly_predictions.csv        # Isolation Forest scores and anomaly predictions
│       ├── anomaly_metrics.csv            # Precision, Recall, F1, FPR benchmark metrics
│       └── anomaly_distribution.png       # Anomaly counts and decision score distribution
├── models/
│   ├── best_energy_model.joblib           # Trained serialized best model (XGBoost)
│   └── feature_columns.json               # Input feature schema used by the forecasting model
├── src/
│   ├── load_data.py                       # SQLite database loader
│   ├── clean_data.py                      # Data validation & test fixture filter
│   ├── feature_engineering.py             # Feature creation & chronological split
│   ├── train_models.py                    # End-to-end forecasting training & evaluation
│   └── anomaly_detection.py               # Isolation Forest anomaly detection pipeline
├── notebooks/
│   └── 01_data_exploration_and_validation.ipynb
├── requirements.txt                       # Dedicated AI module dependencies
└── README.md                              # Comprehensive AI documentation
```

---

## 3. Energy Consumption Forecasting (Day 6 Summary)

### 3.1. Models Evaluated (Chronological Test Set: $N = 125$)

| Model | MAE (kWh) | RMSE (kWh) | $R^2$ Score | Rank (by MAE) |
| :--- | :---: | :---: | :---: | :---: |
| **XGBoost Regressor** *(Best)* | **1.077848** | **2.586846** | **+0.056597** | **1** |
| **Random Forest Regressor** | **1.078309** | **2.574246** | **+0.065764** | 2 |
| **Persistence Baseline** | 1.216042 | 3.044808 | -0.307002 | 3 (Reference) |
| **Linear Regression** | 1.398776 | 3.417494 | -0.646539 | 4 |

---

## 3.5. Prediction API Integration (Day 9)

The best performing model (XGBoost) was integrated into the FastAPI backend on **Day 9**.

### Architecture
- **Separate Router**: A dedicated `prediction.py` router with the `/api/prediction` prefix was created to avoid duplicate routes and ensure a clean separation from the existing energy data endpoints.
- **On-Request Inference**: Predictions are generated on-the-fly and are not stored in the database, preserving the Day 8 schema.
- **Dynamic Feature Derivation**: The prediction service extracts the last 3 historical readings from SQLite to derive all required 15 features (including time and rolling mean features) without requiring any future data.
- **Frontend Integration**: A new `PredictionPanel` component in the React dashboard dynamically displays the AI's predicted next energy usage for each device.

---

## 4. Anomaly Detection (Day 7)

### 4.1. Anomaly Detection Method: Isolation Forest
Unsupervised **Isolation Forest** was chosen as the primary anomaly detection algorithm because:
- **Tree-Based Partitioning**: Isolates anomalies instead of profiling normal points, making it fast, robust, and highly sensitive to outliers in high-dimensional telemetry.
- **No Reliance on Normal Labels**: Operates without requiring prior ground-truth anomaly annotations in the clean campus dataset.
- **Computational Efficiency**: Scales linearly with data size ($O(n)$) and works well for real-time edge or server deployment.

### 4.2. Selected Features (8 Features)
Features were chosen to detect both instantaneous electrical spikes and contextual occupancy/schedule discrepancies:
- `power` (W): Direct indicator of consumption spikes.
- `current` (A): Physical current draw.
- `voltage` (V): Grid stability and over/under-voltage fluctuations.
- `temperature` (°C): Ambient room temperature.
- `occupancy`: Occupancy count in the zone.
- `hour`: Time of day (distinguishes off-hours vs. active hours).
- `energy_delta` (kWh): Step-to-step energy surge.
- `power_rolling_mean_3` (W): 3-step moving average of active power.

### 4.3. Synthetic Anomaly Generation Rules
Because the clean baseline telemetry represents normal operating conditions, a dedicated, separate synthetic evaluation dataset (`ai/data/anomaly/synthetic_anomalies.csv`) was generated with **24 injected anomalies** (~4% of the dataset) across 4 realistic failure scenarios:

1. **Sudden Power Spike (`power_spike`)**:
   - Power multiplied by $3.5\times - 4.8\times$ with corresponding current surges (simulates equipment short/overload).
2. **Off-Hours Phantom Load (`off_hours_high_load`)**:
   - High power ($1800\text{W} - 2500\text{W}$) between 01:00 and 04:00 with zero occupancy (simulates HVAC or lab PCs left running overnight).
3. **Voltage Instability (`voltage_anomaly`)**:
   - Severe voltage sag ($175\text{V} - 185\text{V}$) or surge ($270\text{V} - 285\text{V}$) with high current draw ($8\text{A} - 12.5\text{A}$).
4. **Energy Surge with Zero Occupancy (`energy_delta_surge`)**:
   - Step energy consumption rate accelerated by $10\times$ while occupancy is 0.

### 4.4. Benchmark Evaluation Results (Synthetic Test Set: $N = 629$)

| Metric | Measured Value | Interpretation |
| :--- | :---: | :--- |
| **Total Evaluation Records** | `629` | 605 normal + 24 synthetic anomalies |
| **Normal Records (Ground Truth)** | `605` | Clean baseline records |
| **Synthetic Anomalies (Ground Truth)**| `24` | Injected abnormal patterns |
| **True Positives (TP)** | `22` | Abnormal records correctly flagged |
| **False Positives (FP)** | `25` | Normal records flagged as anomalies |
| **True Negatives (TN)** | `580` | Normal records correctly identified |
| **False Negatives (FN)** | `2` | Abnormal records missed |
| **Precision** | **46.81%** (`0.468085`) | Tradeoff due to conservative contamination |
| **Recall (Sensitivity)** | **91.67%** (`0.916667`) | High sensitivity catching 22/24 anomalies |
| **F1-Score** | **61.97%** (`0.619718`) | Harmonic mean of precision and recall |
| **False Positive Rate (FPR)** | **4.13%** (`0.041322`) | Low false alarm rate (~4%) |
| **Contamination Parameter** | **4.00%** (`0.040000`) | Expected proportion of outliers |

### 4.5. Distinction: Synthetic Benchmark vs. Real-World Operations
- **Controlled Benchmark**: The measured precision, recall, and F1-scores represent detection accuracy on **explicitly injected physical fault rules** and do not claim to reflect naturally occurring campus anomalies.
- **Operational Reality**: In physical deployments, anomalies exhibit greater variability (e.g., gradual sensor drift, harmonic distortion, intermittent loose wiring). The model's anomaly score (`decision_function`) should be used as a triage rank rather than a rigid binary cutoff.

### 4.6. Limitations & Future Work
1. **Unsupervised Contamination Tuning**: Fixed contamination ($0.04$) controls the threshold; dynamic thresholding based on rolling statistics will be explored in production.
2. **Contextual Baselines**: Multi-sensor fusion (e.g., ambient outdoor weather vs. indoor HVAC) will further reduce false positives during campus events.

---

## 5. Anomaly Detection API Integration (Day 10)

The Isolation Forest anomaly model was successfully integrated into the FastAPI backend on **Day 10**.

### Architecture
- **In-Memory Training Initialization**: The `anomaly_service.py` securely loads the clean baseline telemetry data (`ai/data/processed/clean_energy_dataset.csv`) directly on backend startup. It re-trains the exact same Isolation Forest algorithm in-memory to ensure 100% logic parity.
- **Dedicated Router**: Exposed under `backend/app/routes/anomaly.py` via endpoints (`POST /api/anomaly/check` and `GET /api/anomaly/latest`).
- **Real-Time Feature Engineering**: The backend calculates dynamic features such as `energy_delta` and `power_rolling_mean_3` by polling recent state telemetry dynamically and securely handling missing histories. 
- **Frontend Panel Integration**: A sleek `AnomalyPanel` was developed in React (`frontend/src/components/AnomalyPanel.jsx`) to display live anomalies clearly, tracking active faults. 
- **Controlled Test Environment**: Verification relies on controlled payload scripts rather than permanently mutating or corrupting the `clean_energy_dataset.csv` or IoT simulator.
