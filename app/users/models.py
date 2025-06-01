from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, " f"username={self.username!r},"
        )

    def __repr__(self):
        return str(self)
