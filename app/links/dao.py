from datetime import datetime, timezone, timedelta

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from app.links.models import Link, LinkClick
from ..database import async_session


class LinksDAO:
    @classmethod
    async def add(cls, link, orig_link, user_id, session: AsyncSession):
        new_instance = Link(link=link, orig_link=orig_link, creator_id=user_id)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def get_original(cls, link, session: AsyncSession):
        query = select(Link).filter_by(link=link)
        result = await session.execute(query)
        return result.scalar_one_or_none().orig_link


class LinkClicksDAO:
    @classmethod
    async def count_last_day(cls, link_id, session: AsyncSession):
        day_ago = datetime.now() - timedelta(hours=24)
        query = (
            select(func.count())
            .select_from(LinkClick)
            .filter_by(link_id=link_id)
            .where(LinkClick.created_at >= day_ago)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def count_last_hour(cls, link_id, session: AsyncSession):
        hour_ago = datetime.now() - timedelta(hours=1)
        query = (
            select(func.count())
            .select_from(LinkClick)
            .filter_by(link_id=link_id)
            .where(LinkClick.created_at >= hour_ago)
        )

        result = await session.execute(query)
        return result.scalar_one_or_none()
