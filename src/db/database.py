import logging
import time
from collections.abc import Generator

from sqlalchemy import create_engine
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


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_database(max_attempts: int = 10, delay_seconds: float = 2.0) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database schema initialized")
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
