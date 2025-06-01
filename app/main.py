import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from .dependencies import get_session
from .links.dao import LinksDAO
from .links.schemas import LinkInput
from .users.router import router as router_users
from .links.router import router as router_links

app = FastAPI()
app.include_router(router_users)
app.include_router(router_links)


@app.get("/{link}")
async def redirect_to_original(
    request: Request, session: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    link = request.url.__str__()
    try:
        original_link = await LinksDAO.get_original(link, session)
        print(original_link)
        return RedirectResponse(original_link)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
