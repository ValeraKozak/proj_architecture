from src.db.database import _split_sql_statements


def test_split_sql_statements_keeps_do_blocks_intact():
    script = """
    DO $$
    BEGIN
        CREATE TYPE role AS ENUM ('user', 'moderator', 'admin');
    EXCEPTION
        WHEN duplicate_object THEN NULL;
    END $$;

    CREATE TABLE example (
        id INTEGER PRIMARY KEY,
        note TEXT NOT NULL DEFAULT 'hello;world'
    );
    """

    statements = _split_sql_statements(script)

    assert len(statements) == 2
    assert "CREATE TYPE role AS ENUM" in statements[0]
    assert "END $$" in statements[0]
    assert "CREATE TABLE example" in statements[1]


def test_split_sql_statements_preserves_semicolons_inside_quotes():
    script = """
    INSERT INTO example (note) VALUES ('draft;pending');
    INSERT INTO example (note) VALUES ("quoted;identifier");
    """

    statements = _split_sql_statements(script)

    assert len(statements) == 2
    assert "draft;pending" in statements[0]
    assert '"quoted;identifier"' in statements[1]
