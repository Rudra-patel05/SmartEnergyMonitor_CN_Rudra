import './ErrorMessage.css';

function ErrorMessage({ message, onRetry }) {
  return (
    <div className="error-container" id="error-message">
      <div className="error-icon">⚠️</div>
      <h2 className="error-title">Connection Error</h2>
      <p className="error-text">{message || 'Unable to connect to the backend API.'}</p>
      <p className="error-hint">
        Make sure the FastAPI server is running at the configured URL.
      </p>
      {onRetry && (
        <button className="retry-btn" onClick={onRetry} id="retry-btn">
          🔄 Retry
        </button>
      )}
    </div>
  );
}

export default ErrorMessage;
