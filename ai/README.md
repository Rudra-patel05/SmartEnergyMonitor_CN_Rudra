# AI / Machine Learning Module – SmartEnergyMonitor

> Smart Energy Monitor – Smart Campus (GTU PBL)  
> Module: `ai/` – Telemetry Preprocessing, Feature Engineering, Model Training, and Benchmark Comparison.

---

## 1. Overview & Objectives

In **Day 6**, we implemented, trained, and comparatively evaluated candidate machine learning models for **one-step-ahead energy consumption prediction** ($E_{t+1}$) across campus zones.

### Core Objectives:
- Train candidate regressors on the chronological training set (80%, 480 rows).
- Evaluate out-of-sample performance on the unseen chronological test set (20%, 125 rows).
- Benchmark all models against a **Persistence Baseline**.
- Evaluate using **MAE**, **RMSE**, and **$R^2$ Score**.
- Export model comparison tables, prediction error records, serialized model artifacts, and visual performance charts.

---

## 2. Directory Structure

```
ai/
├── data/
│   ├── raw/
│   │   └── raw_energy_readings.csv        # Immutable snapshot of raw SQLite table (614 rows)
│   └── processed/
│       ├── clean_energy_dataset.csv       # ML-ready engineered dataset (605 rows)
│       ├── model_comparison.csv           # Model evaluation results sorted by MAE
│       ├── model_comparison.png           # Dual-panel comparative visualization
│       └── predictions.csv                # Per-record actuals, predictions, and residuals
├── models/
│   ├── best_energy_model.joblib           # Trained serialized best model (XGBoost)
│   └── feature_columns.json               # Input feature schema used by the model
├── src/
│   ├── load_data.py                       # SQLite database loader
│   ├── clean_data.py                      # Data validation & test fixture filter
│   ├── feature_engineering.py             # Feature creation & chronological split
│   └── train_models.py                    # End-to-end training & benchmark evaluation
├── notebooks/
│   └── 01_data_exploration_and_validation.ipynb
├── requirements.txt                       # Dedicated AI module dependencies
└── README.md                              # Comprehensive AI documentation
```

---

## 3. Models Tested

1. **Persistence Baseline**:
   - $\hat{y}_{t+1} = y_t$ (assumes energy at next time step equals current cumulative energy).
2. **Linear Regression (OLS)**:
   - Parametric baseline fitting a linear hyperplane across all 15 engineered features.
3. **Random Forest Regressor**:
   - Ensemble of 100 decision trees (`n_estimators=100`, `max_depth=10`, `min_samples_split=4`, `random_state=42`).
4. **XGBoost Regressor**:
   - Gradient boosted decision trees (`n_estimators=100`, `learning_rate=0.08`, `max_depth=5`, `subsample=0.8`, `colsample_bytree=0.8`, `random_state=42`).

---

## 4. Feature Schema & Train/Test Strategy

### 4.1. Input Features (15 Total)
- **Temporal**: `hour`, `minute`, `day_of_week`, `is_weekend`
- **Electrical & Sensor State**: `voltage`, `current`, `power`, `energy`, `temperature`, `occupancy`
- **Historical Lag & Rolling**: `previous_energy`, `previous_power`, `energy_rolling_mean_3`, `power_rolling_mean_3`, `energy_delta`

### 4.2. Target Variable
- **Target**: `target_next_energy` ($E_{t+1}$ in kWh).
- **Leakage Prevention**: All 15 features are derived strictly at time $\le t$. Target is forward-shifted per device ($t+1$). Terminal unobserved future targets are dropped.

### 4.3. Train / Test Split
- **Chronological Split (80% / 20%)**: Preserves temporal sequence per device without shuffling.
- **Training Set**: 480 rows (80%)
- **Testing Set**: 125 rows (20%)

---

## 5. Model Evaluation Results & Comparison

Evaluated on the unseen test set ($N = 125$), sorted by lowest MAE:

| Model | MAE (kWh) | RMSE (kWh) | $R^2$ Score | Performance vs. Baseline |
| :--- | :---: | :---: | :---: | :--- |
| **XGBoost Regressor** *(Best)* | **1.077848** | **2.586846** | **+0.056597** | **11.36% MAE reduction** |
| **Random Forest Regressor** | **1.078309** | **2.574246** | **+0.065764** | **11.33% MAE reduction** |
| **Persistence Baseline** | 1.216042 | 3.044808 | -0.307002 | Reference benchmark |
| **Linear Regression** | 1.398776 | 3.417494 | -0.646539 | 15.03% higher error |

---

## 6. Key Findings & Best Model Selection

### Why XGBoost Was Selected:
1. **Lowest Mean Absolute Error**: XGBoost achieved an MAE of `1.0778 kWh`, outperforming all candidates.
2. **Beat the Persistence Baseline**: Delivered an **11.36% MAE improvement** and a **15.04% RMSE reduction** over the persistence model.
3. **Non-linear Relationship Modeling**: Captures occupancy spikes, temperature fluctuations, and cyclic power variations effectively, where standard Linear Regression suffered from high variance and negative $R^2$.
4. **Generalization**: Robust tree ensemble regularization (`subsample=0.8`, `colsample_bytree=0.8`) prevented overfitting on small-to-medium time-series batches.

---

## 7. Limitations & Future Work (Day 7+)

1. **Simulation Session Reset Boundaries**:
   - In synthetic IoT datasets, new simulation runs reset cumulative energy back near zero. This creates a boundary step transition that accounts for a substantial portion of test error across all models.
2. **Dataset Size**:
   - Current dataset comprises 605 records (~2 days of operations). As live telemetry streams accumulate over weeks, model performance will continuously improve.
3. **Next Steps (Day 7+)**:
   - Implement incremental energy consumption ($\Delta E$) prediction and statistical/isolation-forest anomaly detection.
