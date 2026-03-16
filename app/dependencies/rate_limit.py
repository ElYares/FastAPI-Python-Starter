"""Simple in-memory rate limiting helpers for authentication endpoints."""

from __future__ import annotations

from collections import defaultdict, deque
from threading import Lock
from time import time

from fastapi import HTTPException, Request, status

from app.config import settings


class InMemoryRateLimiter:
    """Thread-safe sliding-window limiter for low-scale environments."""

    def __init__(self) -> None:
        self._events: dict[str, deque[int]] = defaultdict(deque)
        self._lock = Lock()

    def hit(self, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
        """
        Register an event and decide if the request is allowed.

        Args:
            key: Unique key for a bucket (ip/user/etc.).
            limit: Max requests allowed within the window.
            window_seconds: Sliding window length in seconds.

        Returns:
            tuple[bool, int]: `(allowed, retry_after_seconds)`.
        """
        now = int(time())
        cutoff = now - window_seconds

        with self._lock:
            bucket = self._events[key]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()

            if len(bucket) >= limit:
                retry_after = max(window_seconds - (now - bucket[0]), 1)
                return False, retry_after

            bucket.append(now)
            return True, 0

    def clear(self) -> None:
        """Clear all limiter buckets (used in tests)."""
        with self._lock:
            self._events.clear()


login_rate_limiter = InMemoryRateLimiter()


def enforce_login_rate_limit(request: Request, username: str) -> None:
    """
    Enforce login rate limits by source IP and user identifier.

    Args:
        request: Incoming request object.
        username: Submitted login username (email in this starter).

    Raises:
        HTTPException: If rate limit is exceeded.
    """
    client_ip = request.client.host if request.client else "unknown"
    normalized_user = username.strip().lower() or "anonymous"

    checks = (
        (
            f"login:ip:{client_ip}",
            settings.LOGIN_RATE_LIMIT_ATTEMPTS_PER_IP,
        ),
        (
            f"login:user:{normalized_user}",
            settings.LOGIN_RATE_LIMIT_ATTEMPTS_PER_USER,
        ),
    )

    for key, limit in checks:
        allowed, retry_after = login_rate_limiter.hit(
            key=key,
            limit=limit,
            window_seconds=settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS,
        )
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Please try again later.",
                headers={"Retry-After": str(retry_after)},
            )
