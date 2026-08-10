from sqlalchemy.orm import Session

from app.exceptions.item_not_found import ItemNotFoundError
from app.models.save import Save
from app.repositories.save import SaveRepository
from app.schemas.request.save import SaveCreateRequestModel


class SaveService:
    def __init__(self):
        self._repository = SaveRepository()

    def create(
        self,
        db: Session,
        model: SaveCreateRequestModel,
    ) -> Save:
        return self._repository.create(db, model.name)

    def get(self, db: Session, save_id: int) -> Save:
        result = self._repository.get_by_id(db, save_id)

        if not result:
            raise ItemNotFoundError(Save)

        return result

    def list(
        self,
        db: Session,
    ) -> list[Save]:
        return self._repository.list_all(db)
