from sqlalchemy.orm import Session

from app.models.save import Save


class SaveRepository:
    def create(
        self,
        db: Session,
        name: str,
    ) -> Save:
        save = Save(name=name)
        db.add(save)
        db.commit()
        db.refresh(save)
        return save

    def get_by_id(
        self,
        db: Session,
        save_id: int,
    ) -> Save | None:
        return db.query(Save).filter(Save.id == save_id).first()

    def list_all(
        self,
        db: Session,
    ) -> list[Save]:
        return db.query(Save).all()
