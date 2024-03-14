from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.referral.schema import ReferralOut, GetReferralById, ReferralIn
from infrastructure.database.models import Referral
from infrastructure.database.session import vortex


class ReferralRepository:

    def __init__(self, session: AsyncSession = Depends(vortex.session_local)) -> None:
        self.session = session
        self.model = Referral

    async def get_all(self):
        stmt = select(self.model).order_by(self.model.created_at)
        answer = await self.session.execute(stmt)
        result = answer.scalars().all()
        return list(result)

    async def get_referral(self, cmd: GetReferralById) -> ReferralOut | None:
        stmt = select(self.model).where(self.model.id == cmd.id)
        answer = await self.session.execute(stmt)
        result = answer.scalar_one_or_none()
        return result

    async def create_referral(self, cmd: ReferralIn) -> ReferralOut | None:
        stmt = (
            insert(self.model)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.code,
                self.model.exp_date,
                self.model.is_active,
                self.model.last_time,
                self.model.user_id,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def update_referral(
        self, cmd: ReferralIn, data: GetReferralById
    ) -> ReferralOut | None:
        stmt = (
            update(self.model)
            .where(self.model.id == data.id)
            .values(**cmd.model_dump())
            .returning(
                self.model.id,
                self.model.code,
                self.model.exp_date,
                self.model.is_active,
                self.model.last_time,
                self.model.user_id,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result

    async def delete_referral(self, cmd: GetReferralById) -> ReferralOut | None:
        stmt = (
            delete(self.model)
            .where(self.model.id == cmd.id)
            .returning(
                self.model.id,
                self.model.code,
                self.model.exp_date,
                self.model.is_active,
                self.model.last_time,
                self.model.user_id,
                self.model.created_at,
            )
        )
        answer = await self.session.execute(stmt)
        await self.session.commit()
        result = answer.mappings().first()
        return result
