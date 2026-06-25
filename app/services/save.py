from sqlalchemy.orm import Session

from app.schemas.request.save import SaveCreateRequestModel


class SaveService:

    def create(
        self,
        db: Session,
        model: SaveCreateRequestModel,
    ):
        pass

    def get(self, db: Session, save_id: int):
        pass

    def list(
        self,
        db: Session,
    ):
        pass
