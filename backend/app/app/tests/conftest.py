import pytest
from starlette.testclient import TestClient

from app.core import config
from app.main import app as main_app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session")
def test_client():
    return TestClient(main_app)


@pytest.fixture(scope="module")
def superuser_token_headers(test_client):
    return get_superuser_token_headers(test_client)


@pytest.fixture(scope="module")
def normal_user_token_headers(test_client):
    return authentication_token_from_email(test_client, config.EMAIL_TEST_USER)
