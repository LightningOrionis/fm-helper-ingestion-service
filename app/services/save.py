from sqlalchemy.orm import Session

from app.models.save import Save
from app.repositories.save import SaveRepository
from app.schemas.request.save import SaveCreateRequestModel


class SaveService:
    def __init__(self):
        self.repository = SaveRepository()

    def create(
        self,
        db: Session,
        model: SaveCreateRequestModel,
    ) -> Save:
        return self.repository.create(db, model.name)

    def get(self, db: Session, save_id: int) -> Save | None:
        return self.repository.get_by_id(db, save_id)

    def list(
        self,
        db: Session,
    ) -> list[Save]:
        return self.repository.list_all(db)
