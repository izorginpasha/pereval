from sqlalchemy import Column, Integer, Text, JSON, ForeignKey, TIMESTAMP, LargeBinary, String
from sqlalchemy.sql import func
from .base import Base


# Модель для пользователей
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    fam = Column(String)
    otc = Column(String)
    phone = Column(String)
