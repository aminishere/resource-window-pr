# app/models/resource.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, index=True)
