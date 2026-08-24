import './AreaFilter.css';

const AREAS = [
  { value: '', label: 'All Areas' },
  { value: 'Computer Laboratory 1', label: 'Computer Laboratory 1' },
  { value: 'Computer Laboratory 2', label: 'Computer Laboratory 2' },
  { value: 'Classroom 1', label: 'Classroom 1' },
  { value: 'Library', label: 'Library' },
  { value: 'Administrative Office', label: 'Administrative Office' },
];

function AreaFilter({ selectedArea, onAreaChange }) {
  return (
    <div className="area-filter" id="area-filter">
      <label className="filter-label">Filter by Area:</label>
      <div className="filter-buttons">
        {AREAS.map((area) => (
          <button
            key={area.value}
            className={`filter-btn ${selectedArea === area.value ? 'active' : ''}`}
            onClick={() => onAreaChange(area.value)}
            id={`filter-${area.value || 'all'}`}
          >
            {area.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export default AreaFilter;
