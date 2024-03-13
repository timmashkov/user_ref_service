from uuid import UUID

from fastapi import APIRouter, Depends, status

from service.referral_service import ReferralService
from domain.referral.schema import ReferralOut, GetReferralById, ReferralIn

ref_router = APIRouter(prefix="/referral")


@ref_router.get("/all", response_model=list[ReferralOut])
async def show_refs(
    ref_repo: ReferralService = Depends(ReferralService),
) -> list[ReferralOut]:
    return await ref_repo.get_all_referrals()


@ref_router.get("/{ref_id}", response_model=ReferralOut)
async def find_ref(
    ref_id: UUID, ref_repo: ReferralService = Depends(ReferralService)
) -> ReferralOut:
    return await ref_repo.get_referral(cmd=GetReferralById(id=ref_id))


@ref_router.post(
    "/new", response_model=ReferralOut, status_code=status.HTTP_201_CREATED
)
async def add_ref(
    cmd: ReferralIn, ref_repo: ReferralService = Depends(ReferralService)
) -> ReferralOut:
    return await ref_repo.add_referral(cmd=cmd)


@ref_router.patch("/upd/{ref_id}", response_model=ReferralOut)
async def update_ref(
    ref_id: UUID, cmd: ReferralIn, ref_repo: ReferralService = Depends(ReferralService)
) -> ReferralOut:
    return await ref_repo.upd_referral(data=GetReferralById(id=ref_id), cmd=cmd)


@ref_router.delete("/del/{ref_id}", response_model=ReferralOut)
async def delete_ref(
    ref_id: UUID, ref_repo: ReferralService = Depends(ReferralService)
) -> ReferralOut:
    return await ref_repo.del_referral(cmd=GetReferralById(id=ref_id))
