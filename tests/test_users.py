from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Bigger Applications!"}


def test_login():
    response = client.get("/users/getall")
    assert response.status_code == 200
