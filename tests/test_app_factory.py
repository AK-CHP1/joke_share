from joke_share import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_dummy(client):
    rsp = client.get("/dummy")
    assert "Working" in rsp.text