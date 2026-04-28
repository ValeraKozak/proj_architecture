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
          <h1>Bulletin Board Platform</h1>
          <p className="brand-subtitle">
            Оголошення, яким легко довіряти і якими зручно керувати.
          </p>
        </div>
      </div>
      <nav className="nav-links">
        <NavLink to="/">Головна</NavLink>
        <NavLink to="/catalog">Каталог</NavLink>
        <NavLink to="/workspace">Кабінет</NavLink>
      </nav>
      <div className="topbar-actions">
        <NavLink className="secondary-link" to="/catalog">
          Переглянути оголошення
        </NavLink>
        <div className="status-pill">
          {isAuthenticated ? `Ви увійшли як ${userName}` : "Гостьовий режим"}
        </div>
      </div>
    </header>
  );
}
