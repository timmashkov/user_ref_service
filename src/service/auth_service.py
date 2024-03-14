from typing import Any

from fastapi import Depends

from domain.user.schema import (
    GetUserByLogin,
    UserJwtToken,
    GetUserById,
    UserRefreshToken,
)
from domain.user.user_repository import UserTokenRepository, UserRepository
from infrastructure.exceptions.auth_exceptions import Unauthorized
from infrastructure.exceptions.user_exceptions import UserNotFound, WrongPassword
from infrastructure.utils.auth_utils.auth_handler import AuthHandler
from infrastructure.utils.auth_utils.auth_helper import validate_uuid


class AuthService:

    def __init__(
        self,
        token_repository: UserTokenRepository = Depends(UserTokenRepository),
        user_repository: UserRepository = Depends(UserRepository),
        auth_repository: AuthHandler = Depends(AuthHandler),
    ) -> None:
        self.token_repository = token_repository
        self.auth_repository = auth_repository
        self.user_repository = user_repository

    async def login(self, data: GetUserByLogin) -> dict[str, str] | dict[str, Any]:
        user = await self.user_repository.get_user_by_login(cmd=data)
        if not user:
            raise UserNotFound
        if not self.auth_repository.verify_password(
            data.password, data.login, user.password
        ):
            raise WrongPassword
        access_token = self.auth_repository.encode_token(user.id)
        refresh_token = self.auth_repository.encode_refresh_token(user.id)
        try:
            await self.token_repository.update_token(
                data=UserJwtToken(id=user.id, token=refresh_token)
            )
        except Exception as e:
            return {"error": e}
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens

    async def logout(self, refresh_token):
        user_id = self.auth_repository.decode_refresh_token(refresh_token)
        token = await self.token_repository.get_token(cmd=validate_uuid(user_id))
        if not token:
            raise Unauthorized
        if token == refresh_token:
            result = await self.token_repository.delete_token(
                cmd=validate_uuid(user_id)
            )
            return result
        raise Unauthorized

    async def is_auth(self, refresh_token):
        user_id = self.auth_repository.decode_token(refresh_token)
        exist_token = await self.token_repository.get_token(cmd=validate_uuid(user_id))
        if not exist_token:
            raise Unauthorized
        try:
            if exist_token == refresh_token:
                return GetUserById(id=user_id)
            else:
                raise Unauthorized
        except AttributeError:
            raise Unauthorized

    async def refresh_token(self, refresh_token):
        user_id = self.auth_repository.decode_refresh_token(refresh_token)
        exist_token = await self.token_repository.get_token(cmd=validate_uuid(user_id))
        if not exist_token:
            raise Unauthorized
        else:
            if exist_token == refresh_token:
                new_token = self.auth_repository.refresh_token(
                    refresh_token=refresh_token
                )
                await self.token_repository.update_token(
                    data=UserJwtToken(
                        id=validate_uuid(user_id),
                        token=new_token.refresh_token,
                    )
                )
                return UserRefreshToken(
                    access_token=new_token.access_token,
                    refresh_token=new_token.refresh_token,
                )
            else:
                raise Unauthorized
