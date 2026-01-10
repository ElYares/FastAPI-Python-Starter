"""
Unit tests for AuthService.

Validates password hashing/verification and JWT creation behavior.
"""

from app.service.auth_service import AuthService


def test_hash_and_verify_password():
    auth = AuthService()
    hashed = auth.hash_password("123456")
    assert auth.verify_password("123456", hashed) is True
    assert auth.verify_password("wrong", hashed) is False

def test_hash_password_rejects_over_72_bytes():
    auth = AuthService()
    long_pwd = "a" * 100
    import pytest
    with pytest.raises(ValueError):
        auth.hash_password(long_pwd)
