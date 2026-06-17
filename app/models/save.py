from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Save(Base):
    __tablename__ = "save"
    id = Column(Integer, primary_key=True)
    name = Column(String)
