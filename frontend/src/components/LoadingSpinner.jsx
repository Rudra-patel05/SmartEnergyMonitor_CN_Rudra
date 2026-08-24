import './LoadingSpinner.css';

function LoadingSpinner({ message = 'Loading data...' }) {
  return (
    <div className="loading-container" id="loading-spinner">
      <div className="spinner"></div>
      <p className="loading-message">{message}</p>
    </div>
  );
}

export default LoadingSpinner;
