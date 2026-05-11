import { Link, NavLink } from "react-router-dom";

import { topNavItems } from "../lib/ui-demo";

interface HeaderProps {
  isAuthenticated: boolean;
  userName?: string;
  onLogout: () => void;
}

export function Header({ isAuthenticated, userName, onLogout }: HeaderProps) {
  return (
    <header className="site-header">
      <Link className="site-brand" to="/">
        <span className="site-brand__badge">BB</span>
        <span className="site-brand__copy">
          <strong>Bulletin Board</strong>
          <small>Platform</small>
        </span>
      </Link>

      <nav className="site-nav" aria-label="Primary">
        {topNavItems.map((item) => (
          <a href={item.href} key={item.label}>
            {item.label}
          </a>
        ))}
      </nav>

      <div className="site-header__actions">
        <NavLink className="site-header__post" to="/workspace">
          Post an Ad
        </NavLink>
        {isAuthenticated ? (
          <>
            <NavLink className="site-header__signin" to="/workspace">
              {userName ?? "Profile"}
            </NavLink>
            <button className="site-header__logout" type="button" onClick={onLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <NavLink className="site-header__signin" to="/workspace?auth=login">
              Sign in
            </NavLink>
            <NavLink className="site-header__signup" to="/workspace?auth=register">
              Create account
            </NavLink>
          </>
        )}
      </div>
    </header>
  );
}
