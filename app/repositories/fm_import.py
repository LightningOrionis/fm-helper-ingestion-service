from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.fm_import import Import


class ImportRepository:
    def create(self, db: Session, import_params: dict) -> Import:
        import_params["upload_date"] = func.now()

        import_ = Import(**import_params)
        db.add(import_)
        db.commit()
        db.refresh(import_)

        return import_

    def delete(self, db: Session, import_id: int) -> bool:
        result = db.query(Import).filter(import_id == Import.id).delete()
        return result != 0

    def get_latest_version_by_save(self, db: Session, save_id: int, import_type: str) -> bool:
        return (
            db.query(func.max(Import.version))
            .filter(
                and_(
                    save_id == Import.save_id,
                    import_type == Import.import_type,
                )
            )
            .scalar()
        )
