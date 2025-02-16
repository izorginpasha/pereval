from sqlalchemy.future import select
from db.db import db_dependency
from models.pereval import PerevalAdded
from models.users import Users
from datetime import datetime
from models.pereval import PerevalAdded, PerevalImages, Coords, PerevalLevels
from schemas.pereval import PerevalCreate, ResponseMessage, User, Image, Coord, Level, PerevalResponse,PerevalUpdate
import base64
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload


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
        result = await db.execute(
            select(PerevalAdded)
            .options(selectinload(PerevalAdded.user))  # Подгружаем пользователя
            .filter(PerevalAdded.id == pereval_id)
        )
        pereval = result.scalars().first()
        if pereval:
            return {
                "id": pereval.id,
                "date_added": pereval.date_added,
                "beautyTitle": pereval.beautyTitle,
                "title": pereval.title,
                "other_titles": pereval.other_titles,
                "connect": pereval.connect,
                "add_time": pereval.add_time,
                "status": pereval.status,
                "user_id": pereval.user_id,
                "coord_id": pereval.coord_id,
                "level_id": pereval.level_id,
                "user": {
                    "id": pereval.user.id,  # Добавляем id пользователя
                    "name": pereval.user.name,
                    "fam": pereval.user.fam,
                    "otc": pereval.user.otc,
                    "email": pereval.user.email,
                    "phone": pereval.user.phone,
                },
            }
        else:
            raise HTTPException(status_code=404, detail="Pereval not found")

    except Exception as e:
        return ResponseMessage(status=500, message=f"Ошибка подключения к базе данных: {str(e)}", id=None)


async def update_pereval(db: db_dependency, pereval_id: int, pereval: PerevalUpdate) -> PerevalAdded:
    try:
        db_pereval = await get_pereval(db, pereval_id)

        if db_pereval:
            if pereval.status == "new":
                # Обновление данных
                for key, value in pereval.dict(exclude_unset=True).items():
                    setattr(db_pereval, key, value)

                # Сохранение изменений
                await db.commit()
                await db.refresh(db_pereval)
                return ResponseMessage(status=1, message="успешно")
            else:
                return ResponseMessage(status=0, message="status no new")
        else:
            return ResponseMessage(status=0, message="Нет записи с таким id")
    except Exception as e:
        return ResponseMessage(status=500, message=f"Ошибка подключения к базе данных: {str(e)}", id=None)








