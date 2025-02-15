from sqlalchemy.future import select
from db.db import db_dependency
from models.pereval import PerevalAdded
from models.users import Users
from datetime import datetime
from models.pereval import PerevalAdded, PerevalImages, Coords, PerevalLevels
from schemas.pereval import PerevalCreate, ResponseMessage, User, Image, Coord, Level, PerevalResponse
import base64
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


async def create_pereval(db: db_dependency, pereval: PerevalCreate) -> ResponseMessage:
    try:
        # Сохранение координат
        db_coords = Coords(**pereval.coords.dict())
        db.add(db_coords)
        await db.commit()
        await db.refresh(db_coords)

        # Сохранение сложности
        db_levels = PerevalLevels(**pereval.level.dict())
        db.add(db_levels)
        await db.commit()
        await db.refresh(db_levels)

        # Сохранение user
        # Проверка на существующего пользователя по email
        stmt = select(Users).filter_by(email=pereval.user.email)
        result = await db.execute(stmt)
        db_user = result.scalars().first()

        # Если пользователь не найден, создаем нового
        if not db_user:
            try:
                db_users = Users(**pereval.user.dict())
                db.add(db_users)
                await db.commit()
                await db.refresh(db_users)
                db_user = db_users  # Записываем нового пользователя
            except IntegrityError as e:

                raise e  # Пробрасываем ошибку дальше, если не уникальность

        # Создание перевала
        db_pereval = PerevalAdded(
            beautyTitle=pereval.beauty_title,
            title=pereval.title,
            other_titles=pereval.other_titles,
            connect=pereval.connect,
            add_time=pereval.add_time.replace(tzinfo=None),  # Убираем временную зону
            status="new",
            coord_id=db_coords.id,
            level_id=db_levels.id,
            user_id=db_user.id,

        )
        db.add(db_pereval)
        await db.commit()
        await db.refresh(db_pereval)

        # Добавление изображений
        for image in pereval.images:
            db_image = PerevalImages(pereval_id=db_pereval.id, img=image.data)
            db.add(db_image)

        await db.commit()

        # Ответ с успехом
        return ResponseMessage(status=200, message="Отправлено успешно", id=db_pereval.id)

    except Exception as e:
        # В случае ошибки в процессе работы с базой данных
        return ResponseMessage(status=500, message=f"Ошибка подключения к базе данных: {str(e)}", id=None)


async def get_pereval(db: db_dependency, pereval_id: int):
    try:
        stmt = select(PerevalAdded).where(PerevalAdded.id == pereval_id)
        result = await db.execute(stmt)
        pereval = result.scalars().first()

        if not pereval:
            return ResponseMessage(status=404, message="Перевал не найден", id=None)

        # Преобразуем объект в словарь
        pereval_dict = {column.name: getattr(pereval, column.name) for column in PerevalAdded.__table__.columns}



        return pereval_dict


    except Exception as e:
        return ResponseMessage(status=500, message=f"Ошибка подключения к базе данных: {str(e)}", id=None)
