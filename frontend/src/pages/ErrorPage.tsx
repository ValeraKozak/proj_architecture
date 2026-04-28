import { Link, useNavigate, useParams } from "react-router-dom";

interface ErrorPageProps {
  code?: number;
}

const ERROR_COPY: Record<
  number,
  { code: string; title: string; body: string; action: string; scene: "space" | "monster" | "signal" }
> = {
  400: {
    code: "400",
    title: "Запит зійшов з маршруту",
    body: "Схоже, частина параметрів передалась неправильно. Поверніться назад або почніть новий маршрут із каталогу.",
    action: "Повернути маршрут",
    scene: "signal",
  },
  404: {
    code: "404",
    title: "Схоже, ви загубилися у космосі",
    body: "Такої сторінки тут немає. Можливо, посилання застаріло або адреса була введена з помилкою.",
    action: "Повернутись на орбіту",
    scene: "space",
  },
  500: {
    code: "500",
    title: "Сервер прокинув внутрішнього звіра",
    body: "Щось пішло не так на боці сервера. Ми не змогли завершити дію, тож краще спробувати ще раз трохи пізніше.",
    action: "Заспокоїти сервер",
    scene: "monster",
  },
};

export function ErrorPage({ code }: ErrorPageProps) {
  const navigate = useNavigate();
  const params = useParams();
  const numericCode = code ?? (Number(params.code) || 500);
  const copy = ERROR_COPY[numericCode] ?? ERROR_COPY[500];

  return (
    <div className={`error-screen error-screen--${copy.scene}`}>
      <div className="error-screen__backdrop" />
      <section className="error-scene">
        <div className="error-copy">
          <p className="error-copy__kicker">Error {copy.code}</p>
          <h1>{copy.title}</h1>
          <p>{copy.body}</p>
          <div className="error-actions">
            <button className="cta-button" type="button" onClick={() => navigate(-1)}>
              {copy.action}
            </button>
            <Link className="secondary-link" to="/catalog">
              До каталогу
            </Link>
            <Link className="secondary-link" to="/">
              На головну
            </Link>
          </div>
        </div>

        <div className="error-illustration">
          <div className="error-stars" />
          {copy.scene === "space" ? (
            <>
              <div className="error-number error-number--left">{copy.code[0]}</div>
              <div className="error-number error-number--right">{copy.code[2]}</div>
              <div className="astronaut-shell">
                <div className="astronaut">
                  <div className="astronaut__helmet" />
                  <div className="astronaut__body" />
                  <div className="astronaut__arm astronaut__arm--left" />
                  <div className="astronaut__arm astronaut__arm--right" />
                  <div className="astronaut__leg astronaut__leg--left" />
                  <div className="astronaut__leg astronaut__leg--right" />
                </div>
              </div>
            </>
          ) : null}

          {copy.scene === "monster" ? (
            <div className="monster-card">
              <div className="monster">
                <div className="monster__horn monster__horn--left" />
                <div className="monster__horn monster__horn--right" />
                <div className="monster__eye monster__eye--left" />
                <div className="monster__eye monster__eye--right" />
                <div className="monster__mouth" />
                <div className="monster__paw monster__paw--left" />
                <div className="monster__paw monster__paw--right" />
              </div>
              <strong>500</strong>
            </div>
          ) : null}

          {copy.scene === "signal" ? (
            <div className="signal-card">
              <div className="signal-card__bars">
                <span />
                <span />
                <span />
                <span />
              </div>
              <div className="signal-card__wire" />
              <strong>400</strong>
            </div>
          ) : null}
        </div>
      </section>
    </div>
  );
}
