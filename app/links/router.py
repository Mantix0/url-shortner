import string
import random
from typing import List, Literal

from fastapi import APIRouter, status, Depends, Request, Response, HTTPException
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from .dao import LinksDAO, LinkClicksDAO
from ..users.models import User
from .schemas import LinkReturn, LinkStatsReturn
from ..dependencies import get_active_user, get_session

router = APIRouter(prefix="/api/v1/links")


@router.post(
    "/create_alias",
    status_code=status.HTTP_201_CREATED,
    summary="Создать укороченную ссылку",
    tags=["Private"],
)
async def create_link_alias(
    input_link: HttpUrl,
    request: Request,
    user_data: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> LinkReturn:
    orig_link = str(input_link)
    new_link = await LinksDAO.get_link_by_orig(orig_link, session)

    if new_link is None:
        characters = string.ascii_letters + string.digits
        alias = "".join(random.choice(characters) for _ in range(8))
        host = request.base_url
        link = str(host) + alias

        new_link = await LinksDAO.add(link, orig_link, user_data.id, session)

    day_clicks = await LinkClicksDAO.count_last_day(new_link.id, session)
    hour_clicks = await LinkClicksDAO.count_last_hour(new_link.id, session)

    return LinkReturn.model_validate(
        {
            "last_hour_clicks": hour_clicks,
            "last_day_clicks": day_clicks,
            **new_link.__dict__,
        }
    )


@router.get(
    "/selection",
    summary="Получить выборку ссылок",
    tags=["Private"],
)
async def get_link_selection(
    user_data: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
    per_page: int = 50,
    page: int = 0,
    active_only: bool = False,
    unexpired_only: bool = False,
) -> List[LinkReturn]:

    selection = await LinksDAO.get_selection(
        offset=page * per_page,
        limit=page * per_page + per_page,
        active_only=active_only,
        unexpired_only=unexpired_only,
        session=session,
    )

    result_selection = [LinkReturn.model_validate(i.__dict__) for i in selection]

    return result_selection


@router.get(
    "/stats/selection",
    summary="Получить выборку статистики по ссылкам",
    tags=["Private"],
)
async def get_link_stats_selection(
    user_data: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
    per_page: int = 10,
    page: int = 0,
    sort_by: Literal["last_hour_clicks", "last_day_clicks"] = "last_day_clicks",
    desc: bool = True,
) -> List[LinkStatsReturn]:

    selection = await LinksDAO.get_selection(
        offset=page * per_page,
        limit=page * per_page + per_page,
        session=session,
    )

    result_selection = []
    for i in selection:
        day_clicks = await LinkClicksDAO.count_last_day(i.id, session)
        hour_clicks = await LinkClicksDAO.count_last_hour(i.id, session)
        result_selection.append(
            {
                **i.__dict__,
                "last_hour_clicks": hour_clicks,
                "last_day_clicks": day_clicks,
            }
        )

    result_selection.sort(key=lambda x: x[sort_by], reverse=desc)

    result_selection = [LinkStatsReturn.model_validate(i) for i in result_selection]
    return result_selection


@router.patch(
    "/deactivate",
    summary="Деактивировать ссылку",
    tags=["Private"],
)
async def deactivate_link(
    input_link: HttpUrl,
    user_data: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
):
    result = await LinksDAO.deactivate(str(input_link), session)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )
    return {"message": "Link successfully deactivated"}
