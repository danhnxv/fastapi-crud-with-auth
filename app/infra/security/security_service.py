"""Security module"""
from typing import Optional, Union
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from random import sample
from secrets import choice
from string import ascii_letters, digits, ascii_uppercase, ascii_lowercase
from app.config import settings
from app.domain.auth.entity import TokenData

from app.domain.user.entity import UserInDB
from app.infra.database.models.user import User as UserModel
from app.domain.shared.enum import AuthGrantType
from app.infra.user.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token", auto_error=False)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_token(token: str, grant_type: Optional[AuthGrantType] = None) -> Optional[TokenData]:
    try:
        # decode jwt token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # get email from decoded token
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, id=payload.get("id"), grant_type=payload.get("grant_type"))
        if grant_type and grant_type != token_data.grant_type:
            raise credentials_exception
        return token_data
    except JWTError:
        raise credentials_exception


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_random_password(length: int = 20):
    punctuation = "!@#$%^&*"
    alphabet = ascii_letters + digits + punctuation
    requirements = [
        ascii_uppercase,  # at least one uppercase letter
        ascii_lowercase,  # at least one lowercase letter
        digits,  # at least one digit
        punctuation,  # at least one symbol
        *(length - 4) * [alphabet],
    ]  # rest: letters digits and symbols
    return "".join(choice(req) for req in sample(requirements, length))


def _get_current_user(
        token: str = Depends(oauth2_scheme),
        user_repository: UserRepository = Depends(UserRepository),
) -> UserModel:
    token_data = verify_token(token=token)
    # get user from db by email
    user: UserModel = user_repository.get_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def _get_authorization_header_optional(
        token: Optional[str] = Security(OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token", auto_error=False))
) -> str:
    return token if token else None


def _get_current_user_optional(
        user_repository: UserRepository = Depends(UserRepository),
        token: str = Depends(_get_authorization_header_optional),
) -> Optional[UserModel]:
    if token:
        return _get_current_user(token, user_repository)
    return None


def get_current_user(
        user: UserModel = Depends(_get_current_user)
) -> UserModel:
    current_user = UserInDB.model_validate(user)
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    # clone data
    to_encode = data.copy()

    # set token expire time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # create jwt token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    if isinstance(encoded_jwt, str):
        return encoded_jwt
    else:
        return encoded_jwt.decode("utf-8")


class SecurityService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    def get_user(self, username: str) -> Optional[UserModel]:
        user = self.user_repository.get_by_username(username=username)
        return user

    def authenticate_user(self, username: str, password: str) -> Union[UserModel, bool]:
        user = self.get_user(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
