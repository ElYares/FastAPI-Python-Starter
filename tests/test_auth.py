from fastapi.testclient import TestClient
from app.main import app

# Cliente de pruebas para simular llamadas HTTP
client =TestClient(app)

def test_auth_flow():
    """
    Prueba de flujo de auth y acceso a una ruta protegida

    flujo:
    - Se obtiene el token
    - Llama a secure con el token de cabecera
    - Verifia el acceso exitoso y contenido de respuesta
    """

    # Obtener token
    response = client.post("/api/v1/login")
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Acceder a la ruta protegida con el token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/secure", headers=headers)
    assert response.status_code == 200
    assert "Bienvenido" in response.json()["message"]
