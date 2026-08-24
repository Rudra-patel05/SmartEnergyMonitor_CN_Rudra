import axios from 'axios';

// Use the same base URL as the main api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const predictionApi = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,  // Prediction inference may take slightly longer
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch the latest on-request prediction for every device in the database.
 * GET /api/prediction/energy/predictions/latest
 *
 * Returns an array of prediction objects. Each item has either:
 *   { device_id, area, timestamp, predicted_next_energy, model_name, status: 'ok' }
 * or for devices with insufficient history:
 *   { device_id, status: 'error', detail: '...' }
 */
export async function fetchLatestPredictions() {
  const response = await predictionApi.get('/api/prediction/energy/predictions/latest');
  return response.data;
}

/**
 * Fetch a one-step-ahead prediction for a specific device.
 * POST /api/prediction/energy/predict
 *
 * @param {string} deviceId - The device_id to predict for (e.g. "LAB001")
 * @returns {Promise<{device_id, area, timestamp, predicted_next_energy, model_name}>}
 */
export async function fetchPredictionForDevice(deviceId) {
  const response = await predictionApi.post('/api/prediction/energy/predict', {
    device_id: deviceId,
  });
  return response.data;
}

export default predictionApi;
