import pytest


def test_jokes(client):
    response = client.get("/jokes/") # trailing slash is required
    assert response.status_code == 200

@pytest.mark.parametrize("offset, count, results", [
    (0, 5, (5, 5, 45)),
    (5, 10, (10, 15, 35)),
    (42, 10, (8, 50, 0))
])
def test_jokes_get_by_time(client, offset, count, results):
    response = client.get("/jokes/get", query_string={
        "offset": offset,
        "count": count,
        "sortby": "time"
    })
    data = response.json()
    assert len(data["jokes"]) == results[0]
    assert data["next_offset"] == results[1]
    assert data["remaining"] == results[2]


def test_jokes_by_like(client):
    response = client.get("/jokes/get", query_string={
        "offset": 0,
        "count": 10,
        "sortby": "like"
    })

    data = response.json()
    assert len(data["jokes"]) == 10
    assert data["next_offset"] == 10
    assert data["remaining"] == 40
    likes1 = [joke["like_count"] for joke in data["jokes"]] 

    response = client.get("/jokes/get", query_string={
        "offset": 10,
        "count": 5,
        "sortby": "like"
    })

    data = response.json()
    assert len(data["jokes"]) == 5
    assert data["next_offset"] == 15
    assert data["remaining"] == 35
    likes2 = [joke["like_count"] for joke in data["jokes"]] 
    total_likes = likes1 + likes2
    i = 1
    while i < len(total_likes):
        assert total_likes[i] <= total_likes[i-1]
        i += 1
    

    
