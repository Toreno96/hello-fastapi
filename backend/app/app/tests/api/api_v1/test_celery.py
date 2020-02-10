from app.core import config


def test_celery_worker_test(test_client, superuser_token_headers):
    data = {"msg": "test"}
    r = test_client.post(
        f"{config.API_V1_STR}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Word received"
