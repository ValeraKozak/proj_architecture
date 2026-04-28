import { FormEvent, useState } from "react";

interface AuthPanelProps {
  onLogin: (email: string, password: string) => Promise<void>;
  onRegister: (email: string, name: string, password: string) => Promise<void>;
}

export function AuthPanel({ onLogin, onRegister }: AuthPanelProps) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      if (mode === "login") {
        await onLogin(email, password);
      } else {
        await onRegister(email, name, password);
      }
      setPassword("");
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Something went wrong");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="auth-panel">
      <div className="auth-panel__intro">
        <h3>Увійдіть, щоб публікувати, модерувати та відповідати на повідомлення.</h3>
        <p>Один кабінет для продавця, модератора і адміністратора без зайвих кроків.</p>
      </div>
      <div className="auth-tabs">
        <button className={mode === "login" ? "active" : ""} onClick={() => setMode("login")}>
          Увійти
        </button>
        <button
          className={mode === "register" ? "active" : ""}
          onClick={() => setMode("register")}
        >
          Реєстрація
        </button>
      </div>
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          Email
          <input value={email} onChange={(event) => setEmail(event.target.value)} type="email" />
        </label>
        {mode === "register" ? (
          <label>
            Ім&apos;я та прізвище
            <input value={name} onChange={(event) => setName(event.target.value)} />
          </label>
        ) : null}
        <label>
          Пароль
          <input
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            type="password"
          />
        </label>
        {error ? <p className="form-error">{error}</p> : null}
        <button className="cta-button" disabled={busy} type="submit">
          {busy ? "Працюємо..." : mode === "login" ? "Відкрити кабінет" : "Створити акаунт"}
        </button>
      </form>
    </section>
  );
}
