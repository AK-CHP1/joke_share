import os
import tempfile

import pytest
from joke_share import create_app
from joke_share.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), "data.sql")) as f:
    _sql_data = f.read()


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DATABASE": db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_sql_data)
    
    yield app
    os.close(db_fd)
    os.unlink(db_path)



@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

