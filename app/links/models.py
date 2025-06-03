from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Link(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(unique=True, nullable=False)
    orig_link: Mapped[str] = mapped_column(unique=True, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    active: Mapped[bool] = mapped_column(default=True)

    def __str__(self):
        return (
            f"{self.__class__.__name__}(link={self.link}, "
            f"orig_link={self.orig_link!r},"
            f"active={self.active!r},"
        )

    def __repr__(self):
        return str(self)


class LinkClick(Base):
    __tablename__ = "link_clicks"

    id: Mapped[int] = mapped_column(primary_key=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
