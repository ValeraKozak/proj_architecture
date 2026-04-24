import { NavLink } from "react-router-dom";

interface HeaderProps {
  isAuthenticated: boolean;
  userName?: string;
}

export function Header({ isAuthenticated, userName }: HeaderProps) {
  return (
    <header className="topbar">
      <div className="brand-lockup">
        <div className="brand-chip">BB</div>
        <div>
          <p className="eyebrow">Marketplace showcase</p>
          <h1>Bulletin Board Platform</h1>
        </div>
      </div>
      <nav className="nav-links">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/catalog">Catalog</NavLink>
        <NavLink to="/workspace">Workspace</NavLink>
      </nav>
      <div className="status-pill">
        {isAuthenticated ? `Signed in as ${userName}` : "Guest mode"}
      </div>
    </header>
  );
}
