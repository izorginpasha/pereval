from sqlalchemy import Column, Integer, Text, JSON, ForeignKey, TIMESTAMP, LargeBinary, Float, Enum, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
import enum
from sqlalchemy.dialects.postgresql import ENUM

status_enum = ENUM('new', 'pending', 'accepted', 'rejected', name='statusnum', create_type=True)


# Модель для координат
class Coords(Base):
    __tablename__ = "coords"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)

# Модель сложности

class PerevalLevels(Base):
    __tablename__ = "pereval_levels"
    id = Column(Integer, primary_key=True)
    level_winter = Column(Text)
    level_summer = Column(Text)
    level_autumn = Column(Text)
    level_spring = Column(Text)

# Модель для перевалов
class PerevalAdded(Base):
    __tablename__ = "pereval_added"
    id = Column(Integer, primary_key=True, index=True)
    date_added = Column(TIMESTAMP, default=func.now())
    beautyTitle = Column(Text)
    title = Column(Text)
    other_titles = Column(Text)
    connect = Column(Text)
    add_time = Column(TIMESTAMP)
    status = Column(status_enum, default="new")

    # Связь с таблицей координат
    coord_id = Column(Integer, ForeignKey("coords.id"))
    coord = relationship("Coords")

    # Связь с таблицей уровень сложности в разные сезоны
    level_id = Column(Integer, ForeignKey("pereval_levels.id"))
    level = relationship("PerevalLevels")
    # Связь с изображениями
    images = relationship("PerevalImages", back_populates="pereval", cascade="all, delete, delete-orphan")


# Модель для изображений перевалов
class PerevalImages(Base):
    __tablename__ = "pereval_images"
    id = Column(Integer, primary_key=True, index=True)
    date_added = Column(TIMESTAMP, default=func.now())
    img = Column(LargeBinary, nullable=False)
    pereval_id = Column(Integer, ForeignKey("pereval_added.id"))
    pereval = relationship("PerevalAdded", back_populates="images")





