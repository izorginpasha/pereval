from sqlalchemy import Column, Integer, Text, JSON, ForeignKey, TIMESTAMP, LargeBinary, String
from sqlalchemy.sql import func
from .base import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, primary_key=False, unique=True)
    name = Column(String)
