import sqlite3
from unittest.mock import Mock

import pytest

import joke_share.db as db_funcs


def test_get_db(app):
    with app.app_context():
        db = db_funcs.get_db()
        assert db is db_funcs.get_db()

    # Testing if the connection was closed
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")
    
    assert "closed" in str(e.value)


def test_init_db_command(monkeypatch, runner):
    mock_init_db = Mock()
    monkeypatch.setattr(db_funcs, "init_db", mock_init_db)

    result = runner.invoke(args=["init-db"])
    mock_init_db.assert_called_once()
    assert "Initialized" in result.output


