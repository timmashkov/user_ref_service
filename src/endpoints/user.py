from uuid import UUID

from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from domain.user.schema import UserOut, GetUserById, UserIn, UserOutList, GetUserByLogin
from infrastructure.database.models import User
from infrastructure.utils.auth_utils.token_helper import jwt_header
from service.auth_service import AuthService
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


@user_router.post("/login")
async def login_user(
    auth_in: GetUserByLogin, auth_service: AuthService = Depends(AuthService)
):
    return await auth_service.login(data=auth_in)


@user_router.post("/logout")
async def logout_user(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
):
    token = credentials.credentials
    return await auth_service.logout(refresh_token=token)


@user_router.get("/refresh_token")
async def refresh_user_token(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
):
    token = credentials.credentials
    return await auth_service.refresh_token(refresh_token=token)


@user_router.get("/check_auth")
async def check_auth(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
):
    token = credentials.credentials
    return await auth_service.is_auth(refresh_token=token)
