from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.enums.fm_import import ImportType
from app.models.fm_import import Import


class ImportRepository:
    def create(
        self,
        db: Session,
        import_params: dict,
    ) -> Import:
        import_ = Import(**import_params)
        db.add(import_)
        db.commit()
        db.refresh(import_)

        return import_

    def delete(
        self,
        db: Session,
        import_id: int,
    ) -> bool:
        result = db.query(Import).filter(Import.id == import_id).delete()
        db.commit()
        return result != 0

    def get_latest_version_by_save(
        self,
        db: Session,
        save_id: int,
        import_type: ImportType,
    ) -> int | None:
        return (
            db.query(func.max(Import.version))
            .filter(
                and_(
                    Import.save_id == save_id,
                    Import.import_type == import_type,
                )
            )
            .scalar()
        )
