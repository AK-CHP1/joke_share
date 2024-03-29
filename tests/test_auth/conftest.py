"""Contains fixtures necessary for simulation authentication."""
import pytest


class Authorization:
    """Contains functions for simulating login and register behaviour."""

    def __init__(self, client):
        self._client = client
    
    def login(self, username, password):
        return self._client.post("/auth/login", data={
            "handle": username, "password": password
        })
    
    def register(self, name, email, username, password):
        return self._client.post("/auth/register", data={
            "name": name,
            "email": email,
            "username": username,
            "password": password
        })


@pytest.fixture
def auth(client):
    return Authorization(client)