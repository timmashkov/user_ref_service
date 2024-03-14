from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.user.schema import UserIn, UserOut, GetUserById, UserOutList, UserWithRef
from domain.user.user_repository import UserRepository
from infrastructure.cache.redis_handler import CacheService
from infrastructure.database.models import User
from infrastructure.exceptions.auth_exceptions import Unauthorized
from infrastructure.exceptions.user_exceptions import UserAlreadyExist, UserNotFound
from infrastructure.utils.auth_utils.auth_handler import AuthHandler
from infrastructure.utils.mail_utils import send_email
from service.auth_service import AuthService


class UserService:

    def __init__(
        self,
        user_repo: UserRepository = Depends(UserRepository),
        auth_repo: AuthHandler = Depends(AuthHandler),
        auth_service: AuthService = Depends(AuthService),
        cache_repo: CacheService = Depends(CacheService),
    ) -> None:
        self.user_repo = user_repo
        self.auth_repo = auth_repo
        self.auth_service = auth_service
        self.cache_repo = cache_repo
        self._key = str(self.__class__)

    async def add_user(self, data: UserIn) -> UserOut:
        try:
            salted_pass = self.auth_repo.encode_password(
                password=data.password, salt=data.login
            )
            await self.cache_repo.create_cache(
                self._key,
                UserIn(
                    login=data.login,
                    password=salted_pass,
                    email=data.email,
                ),
            )
            answer = await self.user_repo.create_user(
                data=UserIn(
                    login=data.login,
                    password=salted_pass,
                    email=data.email,
                )
            )
            return answer
        except (UniqueViolationError, IntegrityError):
            raise UserAlreadyExist

    async def get_users(self) -> list[UserOutList]:
        answer = await self.user_repo.get_all()
        await self.cache_repo.read_cache(self._key)
        return answer

    async def get_user(self, cmd: GetUserById) -> UserOut:
        answer = await self.user_repo.get_user_by_id(cmd=cmd)
        if answer:
            await self.cache_repo.read_cache(self._key)
            return answer
        raise UserNotFound

    async def change_user(self, data: UserIn, cmd: GetUserById, token) -> UserOut:
        token = await self.auth_service.is_auth(token)
        if not token:
            raise Unauthorized
        if await self.user_repo.get_user_by_id(cmd=cmd):
            await self.cache_repo.create_cache(self._key, data)
            answer = await self.user_repo.update_user(data=data, cmd=cmd)
            return answer
        raise UserNotFound

    async def drop_user(self, cmd: GetUserById, token) -> UserOut:
        token = await self.auth_service.is_auth(token)
        if not token:
            raise Unauthorized
        if await self.user_repo.get_user_by_id(cmd=cmd):
            await self.cache_repo.delete_cache(self._key)
            answer = await self.user_repo.delete_user(cmd=cmd)
            return answer
        raise UserNotFound

    async def get_user_with_referral(self, cmd: GetUserById, token) -> UserWithRef:
        token = await self.auth_service.is_auth(token)
        if not token:
            raise Unauthorized
        answer = await self.user_repo.get_user_with_ref(cmd=cmd)
        if answer:
            return answer
        raise UserNotFound

    async def email_send(self, token, cmd: GetUserById):
        token = await self.auth_service.is_auth(token)
        if not token:
            raise Unauthorized
        answer = await self.user_repo.get_user_with_ref(cmd=cmd)
        if not answer:
            raise UserNotFound
        return await send_email(receiver=answer.email, message=answer.ref_link.code)
