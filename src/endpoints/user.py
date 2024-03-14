from uuid import UUID

from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials

from domain.user.schema import (
    UserOut,
    GetUserById,
    UserIn,
    UserOutList,
    GetUserByLogin,
    UserWithRef,
)
from infrastructure.utils.auth_utils.token_helper import jwt_header
from service.auth_service import AuthService
from service.user_service import UserService

user_router = APIRouter(prefix="/users")


@user_router.get("/all", response_model=list[UserOutList])
async def show_users(
    user_repo: UserService = Depends(UserService),
) -> list[UserOutList]:
    """
    Возвращает список юзеров
    :param user_repo:
    :return:
    """
    return await user_repo.get_users()


@user_router.get("/ref/{user_id}", response_model=UserWithRef)
async def show_user_with_ref(
    user_id: UUID,
    user_repo: UserService = Depends(UserService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> UserWithRef:
    """
    Возвращает юзера вместе с реф. кодом
    :param user_id:
    :param user_repo:
    :param credentials:
    :return:
    """
    token = credentials.credentials
    return await user_repo.get_user_with_referral(
        cmd=GetUserById(id=user_id), token=token
    )


@user_router.get("/{user_id}", response_model=UserOut)
async def find_user(
    user_id: UUID, user_repo: UserService = Depends(UserService)
) -> UserOut:
    """
    Поиск юзера по айди
    :param user_id:
    :param user_repo:
    :return:
    """
    return await user_repo.get_user(cmd=GetUserById(id=user_id))


@user_router.post("/new", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def registration(
    cmd: UserIn, user_repo: UserService = Depends(UserService)
) -> UserOut:
    """
    Создание юзера
    :param cmd:
    :param user_repo:
    :return:
    """
    return await user_repo.add_user(data=cmd)


@user_router.patch("/upd/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID,
    cmd: UserIn,
    user_repo: UserService = Depends(UserService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> UserOut:
    """
    Редактирование юзера
    :param user_id:
    :param cmd:
    :param user_repo:
    :param credentials:
    :return:
    """
    token = credentials.credentials
    return await user_repo.change_user(
        cmd=GetUserById(id=user_id), data=cmd, token=token
    )


@user_router.delete("/del/{user_id}", response_model=UserOut)
async def delete_user(
    user_id: UUID,
    user_repo: UserService = Depends(UserService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
) -> UserOut:
    """
    Удаление юзера
    :param user_id:
    :param user_repo:
    :param credentials:
    :return:
    """
    token = credentials.credentials
    return await user_repo.drop_user(cmd=GetUserById(id=user_id), token=token)


@user_router.post("/login")
async def login_user(
    auth_in: GetUserByLogin, auth_service: AuthService = Depends(AuthService)
):
    """
    Логин
    :param auth_in:
    :param auth_service:
    :return:
    """
    return await auth_service.login(data=auth_in)


@user_router.post("/logout")
async def logout_user(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
):
    """
    Логаут
    :param auth_service:
    :param credentials:
    :return:
    """
    token = credentials.credentials
    return await auth_service.logout(token=token)


@user_router.post("/email")
async def email(
    cmd: GetUserById,
    user_repo: UserService = Depends(UserService),
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
):
    """
    Отправка письма на почту юзера
    :param cmd:
    :param user_repo:
    :param credentials:
    :return:
    """
    token = credentials.credentials
    return await user_repo.email_send(cmd=cmd, token=token)
