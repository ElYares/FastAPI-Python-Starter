from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_not_found_exception():
    response = client.get("/api/v1/not-found")
    assert response.status_code == 404
    assert response.json() == {"error": "El recurso no existe"}


def test_bad_request_exception():
    response = client.get("/api/v1/bad-request")
    assert response.status_code == 400
    assert response.json() == {"error": "Peticion Incorrecta"}


def test_unhandled_exception():
    response = client.get("/api/v1/exception")
    assert response.status_code == 500
    assert response.json() == {"error": "Internal Server Error"}
