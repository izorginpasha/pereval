from pydantic import BaseModel, validator, HttpUrl,EmailStr
from typing import Optional, List
from datetime import datetime
import re
import base64


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

    @validator('data')
    def validate_image_data(cls, value):
        # Проверка на base64 строку с префиксом
        base64_pattern = re.compile(r"^data:image\/(?:png|jpg|jpeg|gif|webp);base64,([A-Za-z0-9+/=]+)$")

        base64_match = base64_pattern.match(value)
        if base64_match:
            value = base64_match.group(1)  # Убираем префикс, если он был

            # Исправление padding (добавление нужного количества символов '=')
            padding_needed = len(value) % 4
            if padding_needed != 0:
                value += "=" * (4 - padding_needed)

            # Проверка на корректность base64 (попытка декодировать)
            try:
                decoded_value = base64.b64decode(value)
                if len(decoded_value) == 0:
                    raise ValueError("Декодированное изображение пустое.")
            except Exception as e:
                raise ValueError(f"Некорректная base64 строка: {str(e)}")

            return value  # Если это корректный base64, возвращаем его

        # Если строка не соответствует base64
        raise ValueError("data должно быть валидным base64")


class User(BaseModel):
    email: EmailStr
    fam: str
    name: str
    otc: str
    phone: str

    @validator('email')
    def validate_email_domain(cls, v):
        # Пример дополнительной проверки на домен
        if not v.endswith('@example.com'):
            raise ValueError('Email должен быть с доменом @example.com')
        return v


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
