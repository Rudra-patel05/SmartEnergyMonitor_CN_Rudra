import './SummaryCards.css';

function SummaryCards({ summary }) {
  if (!summary) return null;

  const cards = [
    {
      id: 'total-readings',
      label: 'Total Readings',
      value: summary.total_readings.toLocaleString(),
      icon: '📊',
      unit: '',
    },
    {
      id: 'avg-power',
      label: 'Average Power',
      value: summary.average_power.toFixed(2),
      icon: '⚡',
      unit: 'W',
    },
    {
      id: 'max-power',
      label: 'Maximum Power',
      value: summary.max_power.toFixed(2),
      icon: '🔺',
      unit: 'W',
    },
    {
      id: 'total-energy',
      label: 'Total Energy',
      value: summary.total_energy.toFixed(4),
      icon: '🔋',
      unit: 'kWh',
    },
  ];

  return (
    <div className="summary-cards" id="summary-cards">
      {cards.map((card) => (
        <div className="summary-card" key={card.id} id={card.id}>
          <div className="card-icon">{card.icon}</div>
          <div className="card-info">
            <span className="card-label">{card.label}</span>
            <span className="card-value">
              {card.value}
              {card.unit && <span className="card-unit"> {card.unit}</span>}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default SummaryCards;
