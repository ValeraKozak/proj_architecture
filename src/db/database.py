import logging
import time
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.core.config import get_settings


class Base(DeclarativeBase):
    pass


logger = logging.getLogger(__name__)
settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine_kwargs = {"future": True, "connect_args": connect_args}
if ":memory:" in settings.database_url:
    engine_kwargs["poolclass"] = StaticPool
engine = create_engine(settings.database_url, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "db" / "migrations"


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _is_sqlite() -> bool:
    return engine.dialect.name == "sqlite"


def _ensure_migration_table(db: Session) -> None:
    db.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    )


def _split_sql_statements(script: str) -> list[str]:
    return [statement.strip() for statement in script.split(";\n") if statement.strip()]


def _apply_sql_migrations(db: Session) -> None:
    _ensure_migration_table(db)
    applied_versions = {
        version
        for (version,) in db.execute(text("SELECT version FROM schema_migrations"))
    }
    for migration_path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if migration_path.name in applied_versions:
            continue
        script = migration_path.read_text(encoding="utf-8")
        for statement in _split_sql_statements(script):
            db.execute(text(statement))
        db.execute(
            text("INSERT INTO schema_migrations (version) VALUES (:version)"),
            {"version": migration_path.name},
        )


def initialize_database(max_attempts: int = 10, delay_seconds: float = 2.0) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            if _is_sqlite():
                Base.metadata.create_all(bind=engine)
            else:
                with SessionLocal.begin() as db:
                    _apply_sql_migrations(db)
            table_names = inspect(engine).get_table_names()
            logger.info("Database schema initialized tables=%s", ",".join(sorted(table_names)))
            return
        except Exception:  # pragma: no cover - integration safety net
            logger.exception(
                "Database initialization failed on attempt %s/%s",
                attempt,
                max_attempts,
            )
            if attempt == max_attempts:
                raise
            time.sleep(delay_seconds)
