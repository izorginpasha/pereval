from pydantic import BaseModel, validator, HttpUrl
from typing import Optional, List
from datetime import datetime
import re

class Coord(BaseModel):
    latitude: float
    longitude: float
    height: int


class Level(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class Image(BaseModel):
    data: str  # Может быть base64 или URL
    title: str

    @validator("data")
    def validate_data(cls, value):
        """Проверяет, является ли `data` валидным base64 или URL"""
        if cls.is_valid_base64(value) or cls.is_valid_url(value):
            return value
        raise ValueError("data должно быть либо валидным base64, либо URL")

    @staticmethod
    def is_valid_base64(s: str) -> bool:
        """Проверяет, является ли строка валидной base64"""
        try:
            # Длина должна быть кратна 4
            if len(s) % 4 != 0:
                return False
            # Попытка декодирования
            base64.b64decode(s, validate=True)
            return True
        except Exception:
            return False

    @staticmethod
    def is_valid_url(s: str) -> bool:
        """Проверяет, является ли строка валидным URL (изображение)"""
        url_pattern = re.compile(r"^https?://.+\.(jpg|jpeg|png|gif|webp)$", re.IGNORECASE)
        return bool(url_pattern.match(s))


class User(BaseModel):
    email: str
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