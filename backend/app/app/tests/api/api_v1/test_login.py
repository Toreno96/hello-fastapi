from app.core import config


def test_get_access_token(test_client):
    login_data = {
        "username": config.FIRST_SUPERUSER,
        "password": config.FIRST_SUPERUSER_PASSWORD,
    }
    r = test_client.post(f"{config.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(test_client, superuser_token_headers):
    r = test_client.post(
        f"{config.API_V1_STR}/login/test-token", headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
