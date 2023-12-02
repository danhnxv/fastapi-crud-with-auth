from typing import Optional
from pydantic import ConfigDict
from datetime import datetime

from app.domain.shared.enum import UserRole
from app.domain.shared.entity import BaseEntity, IDModelMixin, DateTimeModelMixin


class UserBase(BaseEntity):
    username: str
    role: UserRole = UserRole.ADMIN
    fullname: Optional[str] = None


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    # https://docs.pydantic.dev/2.4/concepts/models/#arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)
    hashed_password: Optional[str]


class UserInCreate(BaseEntity):
    username: str
    fullname: Optional[str] = None
    role: UserRole = UserRole.ADMIN
    password: str


class User(UserBase):
    """
    User domain entity
    """
    id: str
    created_at: datetime
