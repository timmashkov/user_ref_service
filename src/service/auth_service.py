from typing import Any

from fastapi import Depends

from domain.user.schema import (
    GetUserByLogin,
    UserJwtToken,
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
        access_token = self.auth_repository.encode_refresh_token(user.id)
        try:
            await self.token_repository.update_token(
                data=UserJwtToken(id=user.id, token=access_token)
            )
        except Exception as e:
            return {"error": e}
        return access_token

    async def logout(self, token):
        user_id = self.auth_repository.decode_refresh_token(token)
        token = await self.token_repository.get_token(cmd=validate_uuid(user_id))
        if not token:
            raise Unauthorized
        if token == token:
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
                return user_id
            else:
                raise Unauthorized
        except AttributeError:
            raise Unauthorized
