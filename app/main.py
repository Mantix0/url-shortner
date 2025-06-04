from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from .config import get_expiration_hours
from .dependencies import get_session
from .links.dao import LinksDAO, LinkClicksDAO
from .users.router import router as router_users
from .links.router import router as router_links

app = FastAPI()
app.include_router(router_users)
app.include_router(router_links)


@app.get("/{link}", summary="Перенаправление по оригинальной ссылке", tags=["Public"])
async def redirect_to_original(
    request: Request, session: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    link = request.url.__str__()
    try:
        link_info = await LinksDAO.get_link(link, session)
        if link_info.active and link_info.created_at >= datetime.now() - timedelta(
            hours=get_expiration_hours()
        ):
            await LinkClicksDAO.add(link_info.id, session)
            return RedirectResponse(link_info.orig_link)
        else:
            raise Exception
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link is inactive or expired"
        )
