from app.core import config
from app.tests.utils.item import create_random_item


def test_create_item(test_client, superuser_token_headers):
    data = {"title": "Foo", "description": "Fighters"}
    response = test_client.post(
        f"{config.API_V1_STR}/items/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item(test_client, superuser_token_headers):
    item = create_random_item()
    response = test_client.get(
        f"{config.API_V1_STR}/items/{item.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id
