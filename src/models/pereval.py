from sqlalchemy import Column, Integer, Text, JSON, ForeignKey, TIMESTAMP, LargeBinary, Float, Enum, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
import enum
from sqlalchemy.dialects.postgresql import ENUM
from .users import Users


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

d
# Модель для изображений перевалов
class PerevalImages(Base):
    __tablename__ = "pereval_images"
    id = Column(Integer, primary_key=True, index=True)
    date_added = Column(TIMESTAMP, default=func.now())
    img = Column(Text, nullable=False)
    pereval_id = Column(Integer, ForeignKey("pereval_added.id"))
    pereval = relationship("PerevalAdded", back_populates="images")





