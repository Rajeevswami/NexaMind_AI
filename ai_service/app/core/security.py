import secrets
from fastapi import Header, HTTPException, status
from app.core.config import settings

async def verify_internal_key(x_internal_api_key: str | None = Header(default=None)) -> None:
    if not settings.internal_api_key or not x_internal_api_key or not secrets.compare_digest(x_internal_api_key, settings.internal_api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing internal API key")

