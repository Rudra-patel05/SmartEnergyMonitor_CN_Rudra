import { useState } from 'react';
import { fetchPredictionForDevice } from '../services/predictionApi';
import './PredictionPanel.css';

/**
 * PredictionPanel — Day 9
 * ========================
 * Displays the latest XGBoost on-request predictions for all devices.
 *
 * Props
 * -----
 * predictions : Array — list returned by GET /api/prediction/energy/predictions/latest
 *   Each item is either:
 *     { device_id, area, timestamp, predicted_next_energy, model_name, status: 'ok' }
 *   or:
 *     { device_id, status: 'error', detail: '...' }
 * loading     : boolean — true while predictions are being fetched
 * error       : string|null — top-level error message if the whole fetch failed
 * onRefresh   : function — callback to re-fetch predictions
 */
function PredictionPanel({ predictions = [], loading = false, error = null, onRefresh }) {
  const [inlineLoading, setInlineLoading] = useState({});
  const [inlineResults, setInlineResults] = useState({});

  // Allow per-device refresh without reloading everything
  const handleDeviceRefresh = async (deviceId) => {
    setInlineLoading((prev) => ({ ...prev, [deviceId]: true }));
    try {
      const result = await fetchPredictionForDevice(deviceId);
      setInlineResults((prev) => ({ ...prev, [deviceId]: { ...result, status: 'ok' } }));
    } catch (err) {
      const detail = err.response?.data?.detail || err.message || 'Prediction failed';
      setInlineResults((prev) => ({
        ...prev,
        [deviceId]: { device_id: deviceId, status: 'error', detail },
      }));
    } finally {
      setInlineLoading((prev) => ({ ...prev, [deviceId]: false }));
    }
  };

  // Merge inline results over the base predictions list
  const mergedPredictions = predictions.map((p) =>
    inlineResults[p.device_id] ? inlineResults[p.device_id] : p
  );

  const okCount = mergedPredictions.filter((p) => p.status === 'ok').length;

  return (
    <section className="prediction-panel" id="prediction-panel" aria-label="AI Energy Predictions">
      {/* Section header */}
      <div className="prediction-header">
        <div className="prediction-title-group">
          <span className="prediction-icon" aria-hidden="true">🤖</span>
          <div>
            <h2 className="prediction-title">AI Energy Predictions</h2>
            <p className="prediction-subtitle">
              One-step-ahead forecasts powered by XGBoost · MAE&nbsp;1.08&nbsp;kWh
            </p>
          </div>
        </div>
        <button
          id="btn-refresh-predictions"
          className="btn-refresh"
          onClick={onRefresh}
          disabled={loading}
          aria-label="Refresh all predictions"
        >
          <span className={`refresh-icon ${loading ? 'spinning' : ''}`}>⟳</span>
          {loading ? 'Refreshing…' : 'Refresh'}
        </button>
      </div>

      {/* Top-level error */}
      {error && !loading && (
        <div className="prediction-error" role="alert">
          <span className="prediction-error-icon">⚠️</span>
          <div>
            <strong>Could not load predictions</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      {/* Loading skeleton */}
      {loading && (
        <div className="prediction-grid">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="prediction-card skeleton" aria-hidden="true">
              <div className="skeleton-line wide" />
              <div className="skeleton-line narrow" />
              <div className="skeleton-line medium" />
            </div>
          ))}
        </div>
      )}

      {/* Prediction cards */}
      {!loading && mergedPredictions.length === 0 && !error && (
        <p className="prediction-empty">
          No devices found in the database. Start the IoT simulator to populate readings.
        </p>
      )}

      {!loading && mergedPredictions.length > 0 && (
        <>
          <p className="prediction-count">
            {okCount} of {mergedPredictions.length} device{mergedPredictions.length !== 1 ? 's' : ''} predicted successfully
          </p>
          <div className="prediction-grid">
            {mergedPredictions.map((item) => (
              <PredictionCard
                key={item.device_id}
                item={item}
                isLoading={!!inlineLoading[item.device_id]}
                onRefresh={() => handleDeviceRefresh(item.device_id)}
              />
            ))}
          </div>
        </>
      )}
    </section>
  );
}


function PredictionCard({ item, isLoading, onRefresh }) {
  if (item.status === 'error') {
    return (
      <div className="prediction-card prediction-card--error" id={`pred-card-${item.device_id}`}>
        <div className="card-device-id">{item.device_id}</div>
        <div className="card-error-msg">
          <span>⚠️</span> {item.detail}
        </div>
        <button
          className="btn-card-refresh"
          onClick={onRefresh}
          disabled={isLoading}
          aria-label={`Retry prediction for ${item.device_id}`}
        >
          {isLoading ? '…' : 'Retry'}
        </button>
      </div>
    );
  }

  return (
    <div className="prediction-card prediction-card--ok" id={`pred-card-${item.device_id}`}>
      {/* Model badge */}
      <div className="card-top-row">
        <span className="model-badge">{item.model_name || 'XGBoost'}</span>
        <button
          className="btn-card-refresh"
          onClick={onRefresh}
          disabled={isLoading}
          aria-label={`Refresh prediction for ${item.device_id}`}
          title="Re-run prediction for this device"
        >
          <span className={isLoading ? 'spinning' : ''}>⟳</span>
        </button>
      </div>

      {/* Device identity */}
      <div className="card-device-id">{item.device_id}</div>
      <div className="card-area">📍 {item.area}</div>

      {/* Predicted value — hero number */}
      <div className="card-prediction-block">
        <span className="pred-label">Predicted Next Energy</span>
        <span className="pred-value">
          {isLoading ? '…' : item.predicted_next_energy?.toFixed(4)}
          <span className="pred-unit"> kWh</span>
        </span>
      </div>

      {/* Timestamp */}
      <div className="card-timestamp">
        🕐 {item.timestamp} UTC
      </div>
    </div>
  );
}


export default PredictionPanel;
