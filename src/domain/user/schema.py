from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr

from domain.referral.schema import ReferralOut


# User schemas
class GetUserById(BaseModel):
    id: UUID


class GetUserByLogin(BaseModel):
    login: str
    password: str


class UserOutList(GetUserById):
    login: str
    email: EmailStr
    created_at: datetime


class UserIn(GetUserByLogin):
    password: str
    email: EmailStr


class UserOut(UserOutList):
    pass


class UserWithRef(UserOut):
    ref_link: ReferralOut | None


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
