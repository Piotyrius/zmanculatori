from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from .models import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: str,
    *,
    is_admin: bool,
    secret_key: str,
    algorithm: str = "HS256",
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=30)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire, "is_admin": is_admin}
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_token(token: str, *, secret_key: str, algorithm: str = "HS256") -> TokenData:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        sub = payload.get("sub")
        if sub is None:
            raise JWTError("Missing subject")
        is_admin = bool(payload.get("is_admin", False))
        return TokenData(sub=sub, is_admin=is_admin)
    except JWTError as exc:
        raise JWTError("Invalid token") from exc



