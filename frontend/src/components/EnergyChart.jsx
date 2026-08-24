import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import './ChartContainer.css';

function EnergyChart({ readings }) {
  if (!readings || readings.length === 0) {
    return (
      <div className="chart-container" id="energy-chart">
        <h2 className="section-title">Energy Consumption Over Time</h2>
        <div className="empty-state">
          <span className="empty-icon">📈</span>
          <p>No data available for chart.</p>
        </div>
      </div>
    );
  }

  // Sort by timestamp ascending for chart and take last 50 readings
  const chartData = [...readings]
    .sort((a, b) => a.timestamp.localeCompare(b.timestamp))
    .slice(-50)
    .map((r) => ({
      time: r.timestamp.split(' ')[1] || r.timestamp,
      energy: r.energy,
      device: r.device_id,
    }));

  return (
    <div className="chart-container" id="energy-chart">
      <h2 className="section-title">Energy Consumption Over Time</h2>
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
            <XAxis
              dataKey="time"
              tick={{ fontSize: 11, fill: 'var(--color-text-secondary)' }}
              tickLine={false}
            />
            <YAxis
              tick={{ fontSize: 11, fill: 'var(--color-text-secondary)' }}
              tickLine={false}
              label={{
                value: 'Energy (kWh)',
                angle: -90,
                position: 'insideLeft',
                style: { fontSize: 12, fill: 'var(--color-text-secondary)' },
              }}
            />
            <Tooltip
              contentStyle={{
                background: 'var(--color-surface)',
                border: '1px solid var(--color-border)',
                borderRadius: '8px',
                fontSize: '0.85rem',
              }}
            />
            <Line
              type="monotone"
              dataKey="energy"
              stroke="var(--color-chart-energy)"
              strokeWidth={2}
              dot={{ r: 3, fill: 'var(--color-chart-energy)' }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default EnergyChart;
