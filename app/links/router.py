import asyncio
import string
import random
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from .dao import LinksDAO, LinkClicksDAO
from .models import User
from .schemas import LinkInput, LinkReturn
from ..dependencies import get_active_user, get_session

router = APIRouter(prefix="/api/v1/links", tags=["Работа со ссылками"])


@router.post("/create_alias")
async def create_link_alias(
    input_link: LinkInput,
    request: Request,
    user_data: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> LinkReturn:

    characters = string.ascii_letters + string.digits
    alias = "".join(random.choice(characters) for _ in range(8))
    host = request.base_url
    link = str(host) + alias

    new_link = await LinksDAO.add(link, str(input_link.link), user_data.id, session)
    day_clicks = await LinkClicksDAO.count_last_day(new_link.id, session)
    hour_clicks = await LinkClicksDAO.count_last_hour(new_link.id, session)

    return LinkReturn.model_validate(
        {
            "last_hour_clicks": hour_clicks,
            "last_day_clicks": day_clicks,
            **new_link.__dict__,
        }
    )
