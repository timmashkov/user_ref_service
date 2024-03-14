from asyncpg import UniqueViolationError
from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from domain.referral.referal_repository import ReferralRepository
from domain.referral.schema import ReferralOut, GetReferralById, ReferralIn, ReferralUpd
from infrastructure.cache.redis_handler import CacheService
from infrastructure.exceptions.auth_exceptions import Unauthorized
from infrastructure.exceptions.referral_exceptions import (
    ReferralAlreadyExist,
    ReferralNotFound,
)
from service.auth_service import AuthService


class ReferralService:
    def __init__(
        self,
        repository: ReferralRepository = Depends(ReferralRepository),
        auth_repo: AuthService = Depends(AuthService),
        cache_repo: CacheService = Depends(CacheService),
    ):
        self.repository = repository
        self.auth_repo = auth_repo
        self.cache_repo = cache_repo
        self._key = str(self.__class__)

    async def get_all_referrals(self, token) -> list[ReferralOut]:
        token = await self.auth_repo.is_auth(token)
        if not token:
            raise Unauthorized
        answer = await self.repository.get_all()
        await self.cache_repo.read_cache(self._key)
        return answer

    async def get_referral(self, cmd: GetReferralById, token) -> ReferralOut:
        token = await self.auth_repo.is_auth(token)
        if not token:
            raise Unauthorized
        answer = await self.repository.get_referral(cmd=cmd)
        if answer:
            await self.cache_repo.read_cache(self._key)
            return answer
        raise ReferralNotFound

    async def add_referral(self, cmd: ReferralIn, token) -> ReferralOut:
        token = await self.auth_repo.is_auth(token)
        if not token:
            raise Unauthorized
        try:
            answer = await self.repository.create_referral(cmd=cmd)
            await self.cache_repo.create_cache(self._key, cmd)
            return answer
        except (UniqueViolationError, IntegrityError):
            raise ReferralAlreadyExist

    async def upd_referral(
        self, cmd: ReferralUpd, data: GetReferralById, token
    ) -> ReferralOut:
        token = await self.auth_repo.is_auth(token)
        if not token:
            raise Unauthorized
        if await self.repository.get_referral(cmd=data):
            await self.cache_repo.create_cache(self._key, cmd)
            answer = await self.repository.update_referral(cmd=cmd, data=data)
            return answer
        raise ReferralNotFound

    async def del_referral(self, cmd: GetReferralById, token) -> ReferralOut:
        token = await self.auth_repo.is_auth(token)
        if not token:
            raise Unauthorized
        if await self.repository.get_referral(cmd=cmd):
            answer = await self.repository.delete_referral(cmd=cmd)
            await self.cache_repo.delete_cache(self._key)
            return answer
        raise ReferralNotFound
