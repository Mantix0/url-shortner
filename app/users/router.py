from fastapi import APIRouter, HTTPException, status, Depends
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from .models import User
from .schemas import (
    UserRegistration,
    UserAuth,
    UserReturn,
)
from .dao import UsersDAO
from .auth import get_password_hash, authenticate_user, create_access_token
from ..dependencies import get_active_user, get_session

router = APIRouter(prefix="/api/v1/users", tags=["Работа с пользователями"])


@router.post("/register/", summary="Зарегистрировать пользователя", tags=["Public"])
async def add_user(
    user_data: UserRegistration, session: AsyncSession = Depends(get_session)
):
    user = await UsersDAO.get_user_by_email(user_data.email, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    await UsersDAO.add(user_dict, session)
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login/", summary="Авторизовать пользователя", tags=["Public"])
async def auth_user(
    response: Response,
    user_data: UserAuth,
    session: AsyncSession = Depends(get_session),
):
    check = await authenticate_user(
        email=user_data.email, password=user_data.password, session=session
    )
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
        )
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(
        key="users_access_token",
        value=access_token,
    )
    return {"message": "Вы успешно авторизованны!"}


@router.get(
    "/current-user/", summary="Получить действующего пользователя", tags=["Private"]
)
async def get_current_user(
    user_data: User = Depends(get_active_user),
) -> UserReturn:
    return UserReturn.model_validate(user_data.__dict__)


@router.post(
    "/logout/", summary="Деактивировать действующего пользователя", tags=["Private"]
)
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}
