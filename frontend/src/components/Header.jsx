import './Header.css';

function Header() {
  return (
    <header className="header" id="dashboard-header">
      <div className="header-content">
        <div className="header-icon">⚡</div>
        <div>
          <h1 className="header-title">Smart Campus Energy Monitor</h1>
          <p className="header-subtitle">Real-time energy consumption dashboard</p>
        </div>
      </div>
    </header>
  );
}

export default Header;
