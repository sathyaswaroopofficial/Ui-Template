"""Authentication dependency applied to every non-public module router.

This is a simple API-key placeholder. Replace with JWT/OAuth (e.g. via your identity
provider) when you add real users -- the rest of the app does not need to change.
"""

from fastapi import Header

from app.core.config import get_settings
from app.core.errors import UnauthorizedError


def require_auth(x_api_key: str | None = Header(default=None)) -> None:
    expected = get_settings().api_key
    if expected and x_api_key != expected:
        raise UnauthorizedError("Missing or invalid API key")
