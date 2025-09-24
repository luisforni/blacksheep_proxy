from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from jose import jwt
from passlib.hash import bcrypt
from app.core.config import settings

ALGO = "HS256"

def hash_password(plain: str) -> str:
    return bcrypt.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.verify(plain, hashed)

def create_access_token(sub: str, claims: Optional[Dict[str, Any]] = None,
                        minutes: int | None = None) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=minutes or settings.JWT_EXPIRES_MIN)
    payload: Dict[str, Any] = {"sub": sub, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    if claims:
        payload.update(claims)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGO)

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGO])
