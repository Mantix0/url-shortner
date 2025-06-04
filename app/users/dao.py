from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select

from app.database import BaseDAO
from app.users.models import User


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def add(cls, user_dict, session: AsyncSession):
        new_instance = cls.model(**user_dict)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def get_user_by_email(cls, email: str, session: AsyncSession):
        query = select(cls.model).filter_by(email=email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_user_by_id(cls, id: int, session: AsyncSession):
        query = select(cls.model).filter_by(id=id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
