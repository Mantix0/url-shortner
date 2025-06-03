from datetime import datetime

from pydantic import BaseModel, Field, AnyHttpUrl, HttpUrl


class LinkReturn(BaseModel):
    link: HttpUrl


class LinkStatsReturn(BaseModel):
    link: HttpUrl
    orig_link: HttpUrl
    last_hour_clicks: int
    last_day_clicks: int
    created_at: datetime
    active: bool
