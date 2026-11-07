import os
import secrets
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY = os.environ.get("PARAGRAF_API_KEY")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(key: str | None = Security(api_key_header)) -> None:
    if API_KEY is None:
        raise HTTPException(status_code=500, detail="Klucz API nie jest skonfigurowany na serwerze")

    if key is None or not secrets.compare_digest(key, API_KEY):
        raise HTTPException(status_code=401, detail="Nieprawidłowy lub brakujący klucz API")