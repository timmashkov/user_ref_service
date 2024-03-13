from uuid import UUID

from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.user.schema import UserIn, UserOut, GetUserById
from domain.user.user_repository import UserRepository
from infrastructure.database.models import User
from infrastructure.exceptions.user_exceptions import UserAlreadyExist, UserNotFound
from service.auth_handler import AuthHandler


class UserService:

    def __init__(
        self,
        user_repo: UserRepository = Depends(UserRepository),
        auth_repo: AuthHandler = Depends(AuthHandler),
    ) -> None:
        self.user_repo = user_repo
        self.auth_repo = auth_repo
        self._key = str(self.__class__)

    async def add_user(self, data: UserIn) -> UserOut:
        try:
            salted_pass = self.auth_repo.encode_password(
                password=data.password, salt=data.login
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

    async def get_users(self) -> list[User]:
        answer = await self.user_repo.get_all()
        return answer

    async def get_user(self, cmd: GetUserById) -> UserOut:
        answer = await self.user_repo.get_user_by_id(cmd=cmd)
        if answer:
            return answer
        raise UserNotFound

    async def change_user(self, data: UserIn, cmd: GetUserById) -> UserOut:
        if await self.user_repo.get_user_by_id(cmd=cmd):
            answer = await self.user_repo.update_user(data=data, cmd=cmd)
            return answer
        raise UserNotFound

    async def drop_user(self, cmd: GetUserById) -> UserOut:
        if await self.user_repo.get_user_by_id(cmd=cmd):
            answer = await self.user_repo.delete_user(cmd=cmd)
            return answer
        raise UserNotFound
