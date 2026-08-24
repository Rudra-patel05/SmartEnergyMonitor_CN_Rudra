import axios from 'axios';

// Use the environment variable for the backend URL, fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch aggregated summary statistics.
 * GET /api/energy/summary
 */
export async function fetchSummary() {
  const response = await api.get('/api/energy/summary');
  return response.data;
}

/**
 * Fetch energy readings with optional area filter.
 * GET /api/energy/readings?area=...&limit=...
 */
export async function fetchReadings(area = '', limit = 100) {
  const params = { limit };
  if (area) {
    params.area = area;
  }
  const response = await api.get('/api/energy/readings', { params });
  return response.data;
}

export default api;
