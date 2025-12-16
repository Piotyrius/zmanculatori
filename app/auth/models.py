from __future__ import annotations

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: EmailStr
    is_admin: bool = False


class LoginRequest(BaseModel):
    email: EmailStr
    password: str




