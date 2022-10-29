from sqlalchemy import Column, Integer, String
from src.database import Base


class IdeaModel(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True)
    text = Column(String(300))
