from sqlalchemy.future import select
from db.db import db_dependency
from models.pereval import PerevalAdded
from models.users import Users
from datetime import datetime
from models.pereval import PerevalAdded, PerevalImages, Coords
from schemas.pereval import PerevalCreate, ResponseMessage,User,Image,Coord,Level
import base64
import uuid
from fastapi import HTTPException


async def create_pereval(db: db_dependency, pereval: PerevalCreate) -> ResponseMessage:
    try:
        # Сохранение координат
        db_coords = Coords(**pereval.coords.dict())
        db.add(db_coords)
        await db.commit()
        await db.refresh(db_coords)

        # Создание перевала
        db_pereval = PerevalAdded(
            beautyTitle=pereval.beauty_title,
            title=pereval.title,
            other_titles=pereval.other_titles,
            connect=pereval.connect,
            add_time=pereval.add_time.replace(tzinfo=None),  # Убираем временную зону
            status="new",
            coord_id=db_coords.id,
            level_winter=pereval.level.winter,
            level_summer=pereval.level.summer,
            level_autumn=pereval.level.autumn,
            level_spring=pereval.level.spring,
        )
        db.add(db_pereval)
        await db.commit()
        await db.refresh(db_pereval)

        # Добавление изображений
        for image in pereval.images:
            # Декодируем изображение из base64
            try:
                image_data = base64.b64decode(image.data, validate=True)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Ошибка при декодировании изображения: {e}")

            # Сохраняем изображение в таблице
            db_image = PerevalImages(pereval_id=db_pereval.id, img=image_data)
            db.add(db_image)

        await db.commit()

        # Ответ с успехом
        return ResponseMessage(status=200, message="Отправлено успешно", id=db_pereval.id)

    except Exception as e:
        # В случае ошибки в процессе работы с базой данных
        return ResponseMessage(status=500, message=f"Ошибка подключения к базе данных: {str(e)}", id=None)

