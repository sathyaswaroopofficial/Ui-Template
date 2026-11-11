def test_create_and_list_items(client):
    res = client.post("/api/v1/items", json={"name": "First", "description": "hello"})
    assert res.status_code == 201
    item = res.json()
    assert item["name"] == "First"

    res = client.get("/api/v1/items")
    assert res.status_code == 200
    assert [i["id"] for i in res.json()] == [item["id"]]


def test_get_missing_item_returns_404(client):
    res = client.get("/api/v1/items/999")
    assert res.status_code == 404
    assert res.json()["error"] == {"code": "not_found", "message": "Item 999 not found"}


def test_validation_error_format(client):
    res = client.post("/api/v1/items", json={"name": ""})
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "validation_error"


def test_delete_item(client):
    item_id = client.post("/api/v1/items", json={"name": "Temp"}).json()["id"]
    assert client.delete(f"/api/v1/items/{item_id}").status_code == 204
    assert client.get(f"/api/v1/items/{item_id}").status_code == 404
