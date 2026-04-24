import pytest
from sqlalchemy import inspect, text

from src.db.database import SessionLocal, engine, initialize_database

pytestmark = pytest.mark.skipif(
    engine.dialect.name != "postgresql",
    reason="PostgreSQL bootstrap checks run only against a PostgreSQL database",
)


def test_postgres_migrations_create_expected_tables():
    initialize_database(max_attempts=1, delay_seconds=0)

    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    assert {"users", "categories", "listings", "messages", "schema_migrations"} <= table_names


def test_postgres_tracks_applied_migrations():
    initialize_database(max_attempts=1, delay_seconds=0)

    with SessionLocal() as db:
        applied_versions = {
            version
            for (version,) in db.execute(text("SELECT version FROM schema_migrations"))
        }

    assert "001_initial_schema.sql" in applied_versions
