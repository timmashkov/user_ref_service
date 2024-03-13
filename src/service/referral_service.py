from fastapi import Depends

from domain.referral.referal_repository import ReferralRepository
from domain.referral.schema import ReferralOut, GetReferralById, ReferralIn


class ReferralService:
    def __init__(self, repository: ReferralRepository = Depends(ReferralRepository)):
        self.repository = repository

    async def get_all_referrals(self) -> list[ReferralOut]:
        answer = await self.repository.get_all()
        return answer

    async def get_referral(self, cmd: GetReferralById) -> ReferralOut:
        answer = await self.repository.get_referral(cmd=cmd)
        return answer

    async def add_referral(self, cmd: ReferralIn) -> ReferralOut:
        answer = await self.repository.create_referral(cmd=cmd)
        return answer

    async def upd_referral(self, cmd: ReferralIn, data: GetReferralById) -> ReferralOut:
        answer = await self.repository.update_referral(cmd=cmd, data=data)
        return answer

    async def del_referral(self, cmd: GetReferralById) -> ReferralOut:
        answer = await self.repository.delete_referral(cmd=cmd)
        return answer
