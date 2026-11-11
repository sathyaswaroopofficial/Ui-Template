from app.core.config import get_settings


def test_api_key_enforced_when_configured(client, monkeypatch):
    monkeypatch.setattr(get_settings(), "api_key", "secret")
    assert client.get("/api/v1/items").status_code == 401
    assert client.get("/api/v1/items", headers={"X-API-Key": "secret"}).status_code == 200
    assert client.get("/health").status_code == 200
