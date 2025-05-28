"""
Pruebas unitarias para el endpoint /users
"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_users_returns_list():
    """
    Verfica que el endpoint /users retorne un status 200
    y que el contenido sea una lista de usuarios con 'id' y 'name'
    """

    response =  client.get("/api/v1/users")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert all("id" in user and "name" in user for user in data)
