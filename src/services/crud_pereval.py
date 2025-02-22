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
        await db.commit()
        await db.refresh(db_pereval)



        # Ответ с успехом
        return ResponseMessage(status=200, message="Отправлено успешно", id=db_pereval.id)

    except Exception as e:
        # В случае ошибки в процессе работы с базой данных
        return ResponseMessage(status=500, message=f"Ошибка подключения к базе данных: {str(e)}", id=None)


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
            return pereval
        else:
            raise HTTPException(status_code=404, detail="Pereval not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к базе данных: {str(e)}")


async def update_pereval(db: db_dependency, pereval_id: int, pereval: PerevalUpdate) -> ResponseMessage:
    try:
        # Получаем ORM-объект из БД
        db_pereval = await get_pereval(db, pereval_id)

        # Проверяем, если запись не найдена
        if db_pereval is None:
            return ResponseMessagePut(state=0, message="Запись не найдена.", status=404)


        # Проверяем статус
        if db_pereval.status != "new":
            return ResponseMessage(status=0, message="Невозможно обновить, так как запись не в статусе 'new'.")
        # Обновляем поля существующего объекта
        db_pereval.beautyTitle = pereval.beauty_title
        db_pereval.title = pereval.title
        db_pereval.other_titles = pereval.other_titles
        db_pereval.connect = pereval.connect
        db_pereval.add_time = pereval.add_time.replace(tzinfo=None)  # Убираем временную зону
        # Обновляем связанные данные координат
        if pereval.coords:  # Проверяем, что coords передан
            db_pereval.coord.latitude = pereval.coords.latitude
            db_pereval.coord.longitude = pereval.coords.longitude
            db_pereval.coord.height = pereval.coords.height

        # Обновляем связанные уровни
        if pereval.level:
            db_pereval.level.level_winter = pereval.level.level_winter
            db_pereval.level.level_summer = pereval.level.level_summer
            db_pereval.level.level_autumn = pereval.level.level_autumn
            db_pereval.level.level_spring = pereval.level.level_spring

        # Обновляем изображения, если они есть
        if pereval.images:
            db_pereval.images.clear()  # Очистим текущие изображения
            for image in pereval.images:
                db_pereval.images.append(PerevalImages(img=image.data))
        # Сохраняем изменения в БД
        await db.commit()
        await db.refresh(db_pereval)

        return ResponseMessage(status=1, message="Запись успешно обновлена.")




    except IntegrityError:

        return {"state": 0, "message": "Ошибка базы данных: Нарушение целостности данных."}


    except ValidationError:

        return {"state": 0, "message": "Некорректные данные. Проверьте ввод и повторите попытку."}


    except Exception as e:

        return {"state": 0, "message": f"Ошибка при обновлении записи: {str(e)}"}

async def get_pereval_user_email(db: db_dependency, user__email: str) -> List[dict]:
    try:
        # Проверяем, существует ли пользователь с таким email
        stmt_user = select(Users).filter(Users.email == user__email)
        result_user = await db.execute(stmt_user)
        db_user = result_user.scalars().first()

        if not db_user:
            raise HTTPException(status_code=404, detail="Пользователь с таким email не найден")

        # Запрос на получение записей PerevalAdded, связанных с этим пользователем
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

        # Преобразуем ORM-модели в Pydantic-модели
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

            json_data = [p.model_dump(mode='json') for p in response_data]

        # Преобразуем Pydantic-объекты в JSON-совместимые словари
        return JSONResponse(content=json_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка подключения к базе данных: {str(e)}")