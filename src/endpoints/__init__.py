from fastapi import APIRouter

from .user import user_router
from .referral import ref_router

main_router = APIRouter(prefix="/api")

main_router.include_router(router=user_router, tags=["Users"])
main_router.include_router(router=ref_router, tags=["Referrals"])
