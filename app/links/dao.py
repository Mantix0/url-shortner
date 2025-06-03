from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select

from app.config import get_expiration_hours
from app.links.models import Link, LinkClick


class LinksDAO:
    @classmethod
    async def add(cls, link, orig_link, user_id, session: AsyncSession) -> Link:
        new_instance = Link(link=link, orig_link=orig_link, creator_id=user_id)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def get_selection(
        cls,
        offset,
        limit,
        session: AsyncSession,
        active_only=False,
        unexpired_only=False,
    ):
        query = select(Link).limit(limit).offset(offset)
        if active_only:
            query = query.filter_by(active=True)
        if unexpired_only:
            query = query.where(
                Link.created_at
                >= datetime.now() - timedelta(hours=get_expiration_hours())
            )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_link(cls, link, session: AsyncSession) -> Link:
        query = select(Link).filter_by(link=link)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_link_by_orig(cls, orig_link, session: AsyncSession) -> Link:
        query = select(Link).filter_by(orig_link=orig_link)
        result = await session.execute(query)
        return result.scalar_one_or_none()


class LinkClicksDAO:
    @classmethod
    async def add(cls, link_id, session: AsyncSession):
        new_instance = LinkClick(link_id=link_id)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def count_last_day(cls, link_id, session: AsyncSession) -> int:
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
    async def count_last_hour(cls, link_id, session: AsyncSession) -> int:
        hour_ago = datetime.now() - timedelta(hours=1)
        query = (
            select(func.count())
            .select_from(LinkClick)
            .filter_by(link_id=link_id)
            .where(LinkClick.created_at >= hour_ago)
        )

        result = await session.execute(query)
        return result.scalar_one_or_none()
