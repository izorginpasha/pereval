from sqlalchemy.future import select
from db.db import db_dependency
from models.pereval import PerevalAdded
from models.users import Users
from datetime import datetime
from models.pereval import PerevalAdded, PerevalImages, Coords, PerevalLevels
from schemas.pereval import PerevalCreate, ResponseMessage, User, Image, Coord, Level, PerevalResponse, PerevalUpdate
import base64
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload
from typing import List
from fastapi.responses import JSONResponse


# Функция создания перевала
async def create_pereval(db: db_dependency, pereval: PerevalCreate) -> ResponseMessage:
    try:
        # Создание объектов координат и уровней
        db_coords = Coords(**pereval.coords.dict())
        db_levels = PerevalLevels(**pereval.level.dict())

        db.add(db_coords)
        db.add(db_levels)

        # Проверка на существующего пользователя
        stmt = select(Users).filter_by(email=pereval.user.email)
        result = await db.execute(stmt)
        db_user = result.scalars().first()

        if not db_user:
            db_user = Users(**pereval.user.dict())
            db.add(db_user)

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

        # Выполнение всех операций в рамках одной транзакции
        await db.commit()

        # Получаем свежие данные после коммита
        await db.refresh(db_pereval)
        await db.refresh(db_coords)
        await db.refresh(db_levels)
        await db.refresh(db_user)

        return ResponseMessage(status=200, message="Отправлено успешно", id=db_pereval.id)

    except IntegrityError as e:
        return ResponseMessage(status=400, message=f"Ошибка уникальности: {str(e)}", id=None)

    except Exception as e:
        return ResponseMessage(status=500, message=f"Ошибка подключения к базе данных: {str(e)}", id=None)


# Функция получения перевала по ID
async def get_pereval(db: db_dependency, pereval_id: int):
    try:
        result = await db.execute(
            select(PerevalAdded)
            .options(joinedload(PerevalAdded.user))  # Подгружаем пользователя
            .options(joinedload(PerevalAdded.coord))  # Подгружаем связанные координаты
            .options(joinedload(PerevalAdded.level))  # Подгружаем связанные уровни
            .options(joinedload(PerevalAdded.images))  # Подгружаем изображения
            .filter(PerevalAdded.id == pereval_id)
        )
        pereval = result.scalars().first()
        if pereval:
            return PerevalResponse(
                id=pereval.id,
                date_added=pereval.date_added,
                beautyTitle=pereval.beautyTitle,
                title=pereval.title,
                other_titles=pereval.other_titles,
                connect=pereval.connect,
                add_time=pereval.add_time,
                status=pereval.status,
                user=User(id=pereval.user.id, name=pereval.user.name, email=pereval.user.email, fam=pereval.user.fam,
                          otc=pereval.user.otc, phone=pereval.user.phone),
                coords=Coord(latitude=pereval.coord.latitude,
                             longitude=pereval.coord.longitude,
                             height=pereval.coord.height),
                level=Level(
                    level_winter=pereval.level.level_winter if pereval.level.level_winter else None,
                    level_summer=pereval.level.level_summer if pereval.level.level_summer else None,
                    level_autumn=pereval.level.level_autumn if pereval.level.level_autumn else None,
                    level_spring=pereval.level.level_spring if pereval.level.level_spring else None
                ),
                images = [Image(data=img.img) for img in pereval.images if img.img]

            )
        else:
            raise HTTPException(status_code=404, detail="Pereval not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к базе данных: {str(e)}")


# Функция обновления перевала
async def update_pereval(db: db_dependency, pereval_id: int, pereval: PerevalUpdate) -> ResponseMessage:
    try:
        # Получаем текущий объект перевала
        result = await db.execute(
            select(PerevalAdded)
            .options(joinedload(PerevalAdded.user))  # Подгружаем пользователя
            .options(joinedload(PerevalAdded.coord))  # Подгружаем связанные координаты
            .options(joinedload(PerevalAdded.level))  # Подгружаем связанные уровни
            .options(joinedload(PerevalAdded.images))  # Подгружаем изображения
            .filter(PerevalAdded.id == pereval_id)
        )
        db_pereval = result.scalars().first()
        print(db_pereval)

        if db_pereval is None:
            return ResponseMessage(status=0, message="Запись не найдена.", status_code=404)

        # Проверяем статус записи
        if db_pereval.status != "new":
            return ResponseMessage(status=0, message="Невозможно обновить, так как запись не в статусе 'new'.")

        # Обновляем перевал
        db_pereval.beautyTitle = pereval.beauty_title
        db_pereval.title = pereval.title
        db_pereval.other_titles = pereval.other_titles
        db_pereval.connect = pereval.connect
        db_pereval.add_time = pereval.add_time.replace(tzinfo=None)

        # Обновление связанных объектов
        if pereval.coords:
            db_pereval.coord.latitude = pereval.coords.latitude
            db_pereval.coord.longitude = pereval.coords.longitude
            db_pereval.coord.height = pereval.coords.height

        if pereval.level:
            db_pereval.level.level_winter = pereval.level.level_winter
            db_pereval.level.level_summer = pereval.level.level_summer
            db_pereval.level.level_autumn = pereval.level.level_autumn
            db_pereval.level.level_spring = pereval.level.level_spring

        # Обновляем изображения
        if pereval.images:
            db_pereval.images.clear()
            for image in pereval.images:
                db_pereval.images.append(PerevalImages(img=image.data))

        # Сохраняем изменения
        await db.commit()
        await db.refresh(db_pereval)

        return ResponseMessage(status=1, message="Запись успешно обновлена.")

    except IntegrityError:
        return ResponseMessage(status=0, message="Ошибка базы данных: Нарушение целостности данных.")

    except Exception as e:
        return ResponseMessage(status=0, message=f"Ошибка при обновлении записи: {str(e)}")


# Функция получения перевалов пользователя по email
async def get_pereval_user_email(db: db_dependency, user__email: str) -> List[dict]:
    try:
        stmt_user = select(Users).filter(Users.email == user__email)
        result_user = await db.execute(stmt_user)
        db_user = result_user.scalars().first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь с таким email не найден")

        stmt_perevals = (
            select(PerevalAdded)
            .options(joinedload(PerevalAdded.user))
            .options(joinedload(PerevalAdded.coord))
            .options(joinedload(PerevalAdded.level))
            .options(joinedload(PerevalAdded.images))
            .filter(PerevalAdded.user_id == db_user.id)
        )

        result_perevals = await db.execute(stmt_perevals)
        perevals = result_perevals.unique().scalars().all()

        if not perevals:
            raise HTTPException(status_code=404, detail="Записи перевалов не найдены")

        # Преобразуем в формат ответа
        response_data = []
        for p in perevals:
            coords = Coord(**p.coord.__dict__) if p.coord else None
            level = Level(**p.level.__dict__) if p.level else None
            user = User(**p.user.__dict__) if p.user else None
            images = [Image(data=image.img) for image in p.images] if p.images else []

            response_data.append(
                PerevalResponse(
                    id=p.id,
                    date_added=p.date_added,
                    beautyTitle=p.beautyTitle,
                    title=p.title,
                    other_titles=p.other_titles,
                    connect=p.connect,
                    add_time=p.add_time,
                    status=p.status,
                    user=user,
                    coords=coords,
                    level=level,
                    images=images
                )
            )

        return JSONResponse(content=[r.model_dump(mode="json") for r in response_data])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к базе данных: {str(e)}")
