from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncAttrs,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer, String
from app.config import get_db_url

SQLALCHEMY_DATABASE_URL = get_db_url()
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
