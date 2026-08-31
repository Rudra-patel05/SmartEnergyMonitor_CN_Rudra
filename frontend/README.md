# Frontend – Smart Campus Energy Monitor Dashboard

> React + Vite web dashboard for the Smart Campus Energy Monitoring System.

## Status: Day 10 – Anomaly Detection Integration ✅

## Tech Stack

- **React** 19.x
- **Vite** 8.x
- **Axios** – HTTP client for API calls
- **Recharts** – Lightweight chart library

## Setup

### Prerequisites
- Node.js 18+ and npm

### Install

```bash
cd frontend
npm install
```

### Run Development Server

```bash
npm run dev
```

The dashboard will be available at **http://localhost:5173**

### Backend URL Configuration

The dashboard connects to the FastAPI backend. The URL is configured via environment variable:

```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

This is set in the `.env` file. To override, create a `.env.local` file or set the variable before running.

**Important:** The FastAPI backend must be running for the dashboard to display data:

```bash
cd backend
uvicorn app.main:app --reload
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          – App header bar
│   │   ├── SummaryCards.jsx    – 4 metric summary cards
│   │   ├── AreaFilter.jsx     – Area filter buttons
│   │   ├── ReadingsTable.jsx  – Recent readings data table
│   │   ├── EnergyChart.jsx    – Energy consumption line chart
│   │   ├── PowerChart.jsx     – Power usage line chart
│   │   ├── LoadingSpinner.jsx – Loading indicator
│   │   ├── ErrorMessage.jsx   – Error state with retry
│   │   ├── PredictionPanel.jsx– AI Energy Predictions component (Day 9)
│   │   ├── PredictionPanel.css– AI Energy Predictions styles (Day 9)
│   │   ├── AnomalyPanel.jsx   – Anomaly Detection component (Day 10)
│   │   └── AnomalyPanel.css   – Anomaly Detection styles (Day 10)
│   ├── pages/
│   │   └── Dashboard.jsx      – Main dashboard page
│   ├── services/
│   │   ├── api.js             – Centralized API client
│   │   ├── predictionApi.js   – Prediction API client (Day 9)
│   │   └── anomalyApi.js      – Anomaly API client (Day 10)
│   ├── App.jsx
│   ├── main.jsx
│   ├── index.css              – Global design tokens
│   └── App.css
├── .env                       – Environment variables
├── package.json
└── README.md
```

## Dashboard Features

1. **Summary Cards** – Total Readings, Average Power, Maximum Power, Total Energy
2. **Area Filter** – Filter data by campus area (5 areas + All)
3. **Energy Chart** – Line chart showing energy consumption over time
4. **Power Chart** – Line chart showing power usage over time
5. **Readings Table** – Tabular view of recent sensor readings
6. **Prediction Panel (Day 9)** – Display AI-predicted next energy usage for each device
7. **Anomaly Panel (Day 10)** – Display active anomalies and anomaly history for the system
8. **Loading State** – Spinner shown while fetching data
9. **Error State** – Clear error message with retry button when backend is down
10. **Empty State** – Graceful handling when no data is available

## API Endpoints Used

| Endpoint | Method | Description |
|---|---|---|
| `/api/energy/summary` | GET | Aggregated summary statistics |
| `/api/energy/readings` | GET | Recent readings (supports `?area=` filter) |
| `/api/prediction/energy/predictions/latest` | GET | Latest AI predictions for all devices (Day 9) |
| `/api/prediction/energy/predict` | POST | Request AI prediction for a specific device (Day 9) |
| `/api/anomaly/latest` | GET | Latest anomaly detection results for all devices (Day 10) |
| `/api/anomaly/check` | POST | Manual check for anomalies on provided data payload (Day 10) |
