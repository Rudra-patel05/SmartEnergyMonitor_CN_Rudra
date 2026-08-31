import React, { useEffect, useState } from 'react';
import { getLatestAnomalies } from '../services/anomalyApi';
import './AnomalyPanel.css';

const AnomalyPanel = ({ onAnomaliesUpdate }) => {
    const [anomalies, setAnomalies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastRefresh, setLastRefresh] = useState(new Date());

    const fetchAnomalies = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getLatestAnomalies();
            setAnomalies(data);
            setLastRefresh(new Date());
            
            // Pass the active anomaly count up to the dashboard if needed
            if (onAnomaliesUpdate) {
                const activeCount = data.filter(d => d.anomaly_flag === 1).length;
                onAnomaliesUpdate(activeCount);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAnomalies();
        
        // Optional: auto-refresh every 60 seconds
        const interval = setInterval(fetchAnomalies, 60000);
        return () => clearInterval(interval);
    }, []);

    const activeAnomalies = anomalies.filter(a => a.anomaly_flag === 1);

    if (error) {
        return (
            <div className="anomaly-panel">
                <div className="anomaly-header">
                    <h3 className="anomaly-title">🚨 ANOMALY DETECTION</h3>
                </div>
                <div style={{ color: '#ef4444' }}>Failed to load anomaly data: {error}</div>
            </div>
        );
    }

    return (
        <div className="anomaly-panel">
            <div className="anomaly-header">
                <h3 className="anomaly-title">
                    🚨 SYSTEM ANOMALIES 
                    {activeAnomalies.length > 0 && (
                        <span className="anomaly-count">{activeAnomalies.length} ACTIVE</span>
                    )}
                </h3>
                <button 
                    className="anomaly-refresh-btn" 
                    onClick={fetchAnomalies}
                    disabled={loading}
                >
                    {loading ? 'Refreshing...' : `Refresh (Last: ${lastRefresh.toLocaleTimeString()})`}
                </button>
            </div>

            {loading && anomalies.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '20px' }}>Loading anomaly status...</div>
            ) : activeAnomalies.length === 0 ? (
                <div className="no-anomalies">
                    ✅ All systems operating within normal parameters. No active anomalies.
                </div>
            ) : (
                <div className="anomaly-list">
                    {activeAnomalies.map((anomaly, idx) => (
                        <div key={idx} className="anomaly-card">
                            <div className="anomaly-card-header">
                                <span className="anomaly-device">{anomaly.device_id}</span>
                                <span className="anomaly-status anomalous">{anomaly.status}</span>
                            </div>
                            <div className="anomaly-details">
                                <div className="anomaly-detail-item">
                                    <span className="anomaly-detail-label">Area:</span>
                                    <span>{anomaly.area}</span>
                                </div>
                                <div className="anomaly-detail-item">
                                    <span className="anomaly-detail-label">Time:</span>
                                    <span>{anomaly.timestamp}</span>
                                </div>
                                <div className="anomaly-detail-item">
                                    <span className="anomaly-detail-label">Score:</span>
                                    <span style={{ fontWeight: 'bold' }}>
                                        {anomaly.anomaly_score.toFixed(4)}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default AnomalyPanel;
