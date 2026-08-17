from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampedMixin

if TYPE_CHECKING:
    from app.models.fm_import import Import


class Save(Base, TimestampedMixin):
    __tablename__ = "save"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String)

    imports: Mapped[list["Import"]] = relationship(
        back_populates="save",
        cascade="all, delete-orphan",
    )
