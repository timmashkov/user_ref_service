from uuid import UUID

from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from infrastructure.utils.auth_utils.token_helper import jwt_header
from service.referral_service import ReferralService
from domain.referral.schema import ReferralOut, GetReferralById, ReferralIn, ReferralUpd

ref_router = APIRouter(prefix="/referral")


@ref_router.get("/all", response_model=list[ReferralOut])
async def show_refs(
    ref_repo: ReferralService = Depends(ReferralService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> list[ReferralOut]:
    token = credentials.credentials
    return await ref_repo.get_all_referrals(token=token)


@ref_router.get("/{ref_id}", response_model=ReferralOut)
async def find_ref(
    ref_id: UUID,
    ref_repo: ReferralService = Depends(ReferralService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> ReferralOut:
    token = credentials.credentials
    return await ref_repo.get_referral(cmd=GetReferralById(id=ref_id), token=token)


@ref_router.post(
    "/new", response_model=ReferralOut, status_code=status.HTTP_201_CREATED
)
async def add_ref(
    cmd: ReferralIn,
    ref_repo: ReferralService = Depends(ReferralService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> ReferralOut:
    token = credentials.credentials
    return await ref_repo.add_referral(cmd=cmd, token=token)


@ref_router.patch("/upd/{ref_id}", response_model=ReferralOut)
async def update_ref(
    ref_id: UUID,
    cmd: ReferralUpd,
    ref_repo: ReferralService = Depends(ReferralService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> ReferralOut:
    token = credentials.credentials
    return await ref_repo.upd_referral(
        data=GetReferralById(id=ref_id), cmd=cmd, token=token
    )


@ref_router.delete("/del/{ref_id}", response_model=ReferralOut)
async def delete_ref(
    ref_id: UUID,
    ref_repo: ReferralService = Depends(ReferralService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> ReferralOut:
    token = credentials.credentials
    return await ref_repo.del_referral(cmd=GetReferralById(id=ref_id), token=token)
