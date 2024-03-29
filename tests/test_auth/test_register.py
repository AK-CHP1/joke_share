import pytest


from joke_share.db import get_db


def test_register_get(client):
    resp = client.get("/auth/register")
    assert resp.status_code == 200


@pytest.mark.parametrize("name, email, username, password, message",[
    ("Thomas Harris", "harrisjacob@example.com", "tharris3344", "_Password23_", "Email already exists"),
    ("David Malan", "davidmalan@harvard.edu", "bennettchristopher", "_passdMalan10_", "Username already exists"),
    ("William James", "james@example2.com", "thisisjames100", "password100", "Weak password"),
    ("Jimmy Carter", "carter1091@gmail", "carterus1234", "thispassA100", "Invalid email"),
    ("Ross Taylor", "ross1212@example.co.in", "#thisIsRoss22", "_Password1234", "Invalid username"),
    ("", "user2312@example.co.in", "", "Mypass1212_", "All fields are required")
])
def test_register_post_invalid(auth, app, name, email, username, password, message):
    with app.app_context():
        response = auth.register(name, email, username, password)
    assert response.status_code == 200
    assert message in response.text


def test_register_post_valid(app, auth):
    response = auth.register("John Doe", "john121@gmail.com", "johndoe1235", "This_isJohn22")
    assert response.headers["Location"] == "/auth/login"
    with app.app_context():
        q = get_db().execute("SELECT * FROM User "
                             "WHERE username = ?", ("johndoe1235",))
        assert q is not None
        


