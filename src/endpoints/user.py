from uuid import UUID

from fastapi import APIRouter, Depends, status

from domain.user.schema import UserOut, GetUserById, UserIn, UserOutList
from infrastructure.database.models import User
from service.user_service import UserService

user_router = APIRouter(prefix="/users")


@user_router.get("/all", response_model=list[UserOutList])
async def show_users(user_repo: UserService = Depends(UserService)) -> list[User]:
    return await user_repo.get_users()


@user_router.get("/{user_id}", response_model=UserOut)
async def find_user(
    user_id: UUID, user_repo: UserService = Depends(UserService)
) -> UserOut:
    return await user_repo.get_user(cmd=GetUserById(id=user_id))


@user_router.post("/new", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def registration(
    cmd: UserIn, user_repo: UserService = Depends(UserService)
) -> UserOut:
    return await user_repo.add_user(data=cmd)


@user_router.patch("/upd/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID, cmd: UserIn, user_repo: UserService = Depends(UserService)
) -> UserOut:
    return await user_repo.change_user(cmd=GetUserById(id=user_id), data=cmd)


@user_router.delete("/del/{user_id}", response_model=UserOut)
async def delete_user(
    user_id: UUID, user_repo: UserService = Depends(UserService)
) -> UserOut:
    return await user_repo.drop_user(cmd=GetUserById(id=user_id))
