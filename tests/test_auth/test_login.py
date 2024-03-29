import pytest

from joke_share.db import get_db
from flask import session


def test_already_present(app):
    with app.app_context():
        db = get_db()
        data = db.execute("SELECT * FROM User WHERE username = ? OR email = ?", ("bennettchristopher", "bennettchristopher")).fetchone()
        assert data is not None


def test_login_get(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


@pytest.mark.parametrize("username, password, message", [
    ("", "passwewe121", "All fields are required"),
    ("myuser123", "password123", "No such username or email exist"),
    ("you@example.com", "Password123", "No such username or email exists"),
    ("bennettchristopher", "thispass123", "Wrong password")
])
def test_login_post_invalid(app, auth, username, password, message):
    response = auth.login(username, password)
    with app.app_context():
        assert message in response.text


def test_login_post_valid(auth, client):
    response = auth.login("bennettchristopher", "tfGfd1bbwzGc")
    assert response.headers["Location"] == "/dummy"
    with client:
        client.get("/dummy")
        assert session["username"] == "bennettchristopher"
    