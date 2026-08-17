from sqlalchemy import Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.fm_import import ImportType, ImportUploadStatus
from app.models.base import Base, TimestampedMixin
from app.models.save import Save


class Import(Base, TimestampedMixin):
    __tablename__ = "fm_import"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[int] = mapped_column(Integer)
    upload_status: Mapped[ImportUploadStatus] = mapped_column(Enum(ImportUploadStatus))
    import_type: Mapped[ImportType] = mapped_column(Enum(ImportType))
    filename: Mapped[str] = mapped_column(String)
    save_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("save.id"),
    )

    save: Mapped[Save] = relationship(
        "Save",
        back_populates="imports",
    )

    __table_args__ = (UniqueConstraint("save_id", "version", "import_type", name="uq_import_save_version_import_type"),)
