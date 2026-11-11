def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_unknown_route_uses_standard_error_format(client):
    res = client.get("/api/v1/does-not-exist")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "http_error"
