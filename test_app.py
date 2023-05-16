import pytest

from app import app


@pytest.fixture()
def client():
    app.config["SECRET_KEY"] = "test_secret"
    app.config["SERVER_NAME"] = "127.0.0.1:5000"

    yield app.test_client()


def test_add_link(client):
    url = "https://example.com/long"
    result = client.post("/link/new", data=dict(url=url), follow_redirects=True)

    assert result.status_code == 200
    assert url.encode("utf-8") in result.data
    assert result.request.path == "/link/list"
