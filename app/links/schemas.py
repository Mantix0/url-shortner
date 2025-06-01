from datetime import datetime

from pydantic import BaseModel, Field, AnyHttpUrl


class LinkInput(BaseModel):
    link: AnyHttpUrl


class LinkReturn(BaseModel):
    link: AnyHttpUrl
    orig_link: AnyHttpUrl
    last_hour_clicks: int
    last_day_clicks: int
    created_at: datetime
    active: bool
