from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from app.database.base import Base
from app.models.save import Save

class Import(Base):
    __tablename__ = "import"
    id = Column(Integer, primary_key=True)
    version = Column(Integer)
    upload_date = Column(DateTime)
    upload_status = Column(String)
    import_type = Column(String)
    filename = Column(String)
    save_id = Column(Integer, ForeignKey(Save.id))
