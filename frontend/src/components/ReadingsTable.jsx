import './ReadingsTable.css';

function ReadingsTable({ readings }) {
  if (!readings || readings.length === 0) {
    return (
      <div className="table-container" id="readings-table">
        <h2 className="section-title">Recent Readings</h2>
        <div className="empty-state">
          <span className="empty-icon">📭</span>
          <p>No readings available.</p>
          <p className="empty-hint">Start the IoT simulator to generate data.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="table-container" id="readings-table">
      <h2 className="section-title">Recent Readings</h2>
      <div className="table-scroll">
        <table className="readings-table">
          <thead>
            <tr>
              <th>Device ID</th>
              <th>Area</th>
              <th>Timestamp</th>
              <th>Voltage (V)</th>
              <th>Current (A)</th>
              <th>Power (W)</th>
              <th>Energy (kWh)</th>
              <th>Occupancy</th>
            </tr>
          </thead>
          <tbody>
            {readings.map((r) => (
              <tr key={r.id}>
                <td className="cell-device">{r.device_id}</td>
                <td>{r.area}</td>
                <td className="cell-timestamp">{r.timestamp}</td>
                <td className="cell-number">{r.voltage.toFixed(1)}</td>
                <td className="cell-number">{r.current.toFixed(2)}</td>
                <td className="cell-number">{r.power.toFixed(2)}</td>
                <td className="cell-number">{r.energy.toFixed(4)}</td>
                <td className="cell-number">{r.occupancy}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ReadingsTable;
