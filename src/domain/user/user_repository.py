from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from domain.user.schema import (
    UserOut,
    GetUserById,
    UserIn,
    UserToken,
    UserJwtToken,
    GetUserByLogin,
    UserWithRef,
)
from infrastructure.database.models import User
from infrastructure.database.session import vortex


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(vortex.session_local)) -> None:
        self.session = session
        self.model = User

    async def get_all(self):
        stmt = select(
            self.model.id, self.model.login, self.model.email, self.model.created_at
        ).order_by(self.model.id)
        answer = await self.session.execute(stmt)
        result = answer.mappings().all()
        return list(result)

    async def get_user_by_id(self, cmd: GetUserById) -> UserOut | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def get_user_by_login(self, cmd: GetUserByLogin) -> UserOut | None:
        stmt = select(self.model).where(self.model.login == cmd.login)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create_user(self, data: UserIn) -> UserOut | None:
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.password,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_user(self, data: UserIn, cmd: GetUserById) -> UserOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == cmd.id)
            .values(**data.model_dump())
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.password,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_user(self, cmd: GetUserById) -> UserOut | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == cmd.id)
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.password,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def get_user_with_ref(self, cmd: GetUserById) -> UserWithRef | None:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.ref_link))
            .where(self.model.id == cmd.id)
        )
        answer = await self.session.execute(stmt)
        result = answer.unique().scalar_one_or_none()
        return result


class UserTokenRepository:

    def __init__(self, session: AsyncSession = Depends(vortex.session_local)) -> None:
        self.session = session
        self.model = User

    async def update_token(self, data: UserJwtToken):
        stmt = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(token=data.token)
            .returning(
                self.model.id,
                self.model.login,
                self.model.email,
                self.model.password,
                self.model.created_at,
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        answer = result.mappings().first()
        return answer

    async def get_token(self, cmd: UUID) -> UserToken | None:
        stmt = select(self.model.token).where(self.model.id == cmd)
        result = await self.session.execute(stmt)
        answer = result.scalar_one_or_none()
        return answer

    async def delete_token(self, cmd: str):
        stmt = (
            update(self.model)
            .where(self.model.id == cmd)
            .values(token="")
            .returning(self.model.id, self.model.token)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        answer = result.mappings().first()
        return answer
