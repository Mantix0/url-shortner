from datetime import datetime, timezone

from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_auth_data
from app.database import async_session
from fastapi import Request, HTTPException, status, Depends

from app.users.dao import UsersDAO


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
    await session.close()


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def get_active_user(
    token: str = Depends(get_token), session: AsyncSession = Depends(get_session)
):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный!"
        )

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя"
        )

    user = await UsersDAO.get_user_by_id(int(user_id), session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
