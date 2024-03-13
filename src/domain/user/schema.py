from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


# User schemas
class GetUserById(BaseModel):
    id: UUID


class GetUserByLogin(BaseModel):
    login: str


class UserOutList(GetUserById, GetUserByLogin):
    email: EmailStr
    created_at: datetime


class UserIn(GetUserByLogin):
    password: str
    email: EmailStr


class UserOut(UserOutList):
    pass


# Token Schemas
class UserAccessToken(BaseModel):
    access_token: str


class UserTokens(UserAccessToken):
    refresh_token: str


class UserRefreshToken(UserTokens): ...


class UserToken(BaseModel):
    token: str


class UserJwtToken(UserToken):
    id: UUID | str
    token: str = None
