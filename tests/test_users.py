"""
Pruebas para el endpoint /users.

Nota:
- Usamos el fixture `client` de conftest.py para asegurar DB aislada y overrides.
"""

from __future__ import annotations


def test_get_users_returns_list(client):
    """
    Verifica que el endpoint /users retorne 200 y una lista de usuarios
    con campos mínimos esperados.
    """
    response = client.get("/api/v1/users")
    assert response.status_code == 200, response.text

    data = response.json()
    assert isinstance(data, list)

    # Contrato actual: id + email (y opcionalmente full_name/is_active)
    assert all("id" in user and "email" in user for user in data)
