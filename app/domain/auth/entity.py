from typing import Optional
from pydantic import BaseModel, EmailStr
from app.domain.shared.entity import BaseEntity
from app.domain.shared.enum import AuthGrantType
from app.domain.user.entity import User


class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: str = None
    username: str = None
    grant_type: Optional[AuthGrantType] = AuthGrantType.ACCESS_TOKEN


class AuthInfo(BaseEntity):
    username: Optional[str] = None


class UserInLogin(AuthInfo):
    username: Optional[str] = None
    password: Optional[str] = None


class AuthInfoInResponse(BaseEntity):
    token: Token
    user: User
