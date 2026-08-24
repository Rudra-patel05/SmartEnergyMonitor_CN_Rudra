import { useState, useEffect, useCallback } from 'react';
import { fetchSummary, fetchReadings } from '../services/api';
import Header from '../components/Header';
import SummaryCards from '../components/SummaryCards';
import AreaFilter from '../components/AreaFilter';
import ReadingsTable from '../components/ReadingsTable';
import EnergyChart from '../components/EnergyChart';
import PowerChart from '../components/PowerChart';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import './Dashboard.css';

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [readings, setReadings] = useState([]);
  const [selectedArea, setSelectedArea] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(async (area = selectedArea) => {
    setLoading(true);
    setError(null);
    try {
      // Fetch summary and readings in parallel
      const [summaryData, readingsData] = await Promise.all([
        fetchSummary(),
        fetchReadings(area, 100),
      ]);
      setSummary(summaryData);
      setReadings(readingsData);
    } catch (err) {
      console.error('Failed to fetch data:', err);
      const message =
        err.code === 'ERR_NETWORK' || err.code === 'ECONNABORTED'
          ? 'Cannot connect to the backend server. Please ensure FastAPI is running.'
          : err.response?.data?.detail || err.message || 'An unexpected error occurred.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [selectedArea]);

  // Load data on mount
  useEffect(() => {
    loadData('');
  }, []);

  // Reload data when area filter changes
  const handleAreaChange = (area) => {
    setSelectedArea(area);
    loadData(area);
  };

  const handleRetry = () => {
    loadData(selectedArea);
  };

  return (
    <div className="dashboard" id="dashboard">
      <Header />
      <main className="dashboard-content">
        {loading && <LoadingSpinner />}

        {error && !loading && (
          <ErrorMessage message={error} onRetry={handleRetry} />
        )}

        {!loading && !error && (
          <>
            <SummaryCards summary={summary} />
            <AreaFilter selectedArea={selectedArea} onAreaChange={handleAreaChange} />
            <div className="charts-grid">
              <EnergyChart readings={readings} />
              <PowerChart readings={readings} />
            </div>
            <ReadingsTable readings={readings} />
          </>
        )}
      </main>
      <footer className="dashboard-footer">
        <p>Smart Campus Energy Monitor &copy; {new Date().getFullYear()} &mdash; CN Project</p>
      </footer>
    </div>
  );
}

export default Dashboard;
