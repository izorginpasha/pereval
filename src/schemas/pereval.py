from pydantic import BaseModel, validator, HttpUrl, EmailStr
from typing import Optional, List
from datetime import datetime
import re
import base64
from urllib.parse import urlparse


class Coord(BaseModel):
    latitude: float
    longitude: float
    height: int


class Level(BaseModel):
    level_winter: Optional[str] = None
    level_summer: Optional[str] = None
    level_autumn: Optional[str] = None
    level_spring: Optional[str] = None


class Image(BaseModel):
    data: str  # Может быть base64 или URL
    title: str

    @validator('data')
    def validate_image_data(cls, value):
        # Проверка на валидность URL с использованием urllib
        parsed_url = urlparse(value)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("data должно быть валидным URL")
        return value


class User(BaseModel):

    email: EmailStr
    fam: str
    name: str
    otc: str
    phone: str


class PerevalCreate(BaseModel):
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    user: User
    coords: Coord
    level: Level
    images: List[Image]


class ResponseMessage(BaseModel):
    status: int
    message: Optional[str] = None
    id: Optional[int] = None


class PerevalResponse(BaseModel):
    id: int
    date_added: datetime
    beautyTitle: str
    title: str
    other_titles: str
    connect: str
    add_time: datetime
    status: str
    user_id: Optional[int]
    coord_id: int
    level_id: int
    user: Optional[User]  # Теперь добавляем данные пользователя

    class Config:
        orm_mode = True


class PerevalUpdate(BaseModel):
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    coords: Coord
    level: Level
    images: List[Image]


    class Config:
        orm_mode = True