from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_sanity():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_check_no_catches():
    response = client.get("/check")
    assert response.status_code == 200
    assert response.json() == {"catches": 0}