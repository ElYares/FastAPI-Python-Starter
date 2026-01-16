"""
Pytest fixtures for the FastAPI starter.

Key goals:
- Ensure debug routes are mounted during tests by forcing DEV env vars BEFORE app import.
- Provide an isolated SQLite in-memory database for repeatable test runs.
- Override the application's get_db dependency to use the test session.
"""

from __future__ import annotations

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# IMPORTANT: set env vars BEFORE importing app.main/settings
os.environ["APP_ENV"] = os.getenv("APP_ENV", "development")
os.environ["DEBUG"] = os.getenv("DEBUG", "true")


@pytest.fixture(scope="session")
def engine():
    """
    SQLite in-memory engine shared across the whole test session.

    StaticPool keeps the same in-memory DB alive across connections.
    """
    # Lazy import here so env vars above are already applied before settings load.
    from app.dependencies.db import Base  # noqa: WPS433

    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture()
def db_session(engine):
    """
    Database session per test.

    Each test runs in a transaction that is rolled back at the end.
    """
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture()
def client(db_session) -> Generator[TestClient, None, None]:
    """
    FastAPI TestClient fixture with dependency override for get_db.

    This fixture imports the app lazily to guarantee environment variables
    are set before app.main/config settings are evaluated.
    """
    # Lazy imports so settings/app are evaluated AFTER env vars are set.
    from app.main import app  # noqa: WPS433
    from app.dependencies.db import get_db  # noqa: WPS433

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db

    with TestClient(app, raise_server_exceptions=False) as c:
        yield c

    app.dependency_overrides.clear()
