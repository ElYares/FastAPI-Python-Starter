"""
Pytest fixtures for the FastAPI starter.

Provides a TestClient fixture so tests can call the API without spinning up a server.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """
    FastAPI test client fixture.

    Returns:
        TestClient: client instance bound to the FastAPI app.
    """
    return TestClient(app, raise_server_exceptions=False)
