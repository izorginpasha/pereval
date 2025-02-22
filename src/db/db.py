from fastapi import Depends
from sqlalchemy.ext.asyncio import (async_sessionmaker,
                                    create_async_engine,
                                    AsyncSession, AsyncEngine, AsyncConnection)

from core.config import app_settings
from typing import Union, Callable, Annotated


class InternalError(Exception):
    pass


# Функция get_async_session используется для получения асинхронной сессии SQLAlchemy
# Функция get_async_session используется для получения асинхронной сессии SQLAlchemy
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except InternalError:
            await session.rollback()  # Откат транзакции в случае ошибки
            raise  # Пробрасывание ошибки дальше
        finally:
            await session.close()  # Гарантированное закрытие сессии после завершения работы


# Функция create_sessionmaker создаёт фабрику сессий для асинхронной работы с базой данных
def create_sessionmaker(
        bind_engine: Union[AsyncEngine, AsyncConnection]
) -> Callable[..., async_sessionmaker]:
    # Возвращается фабрика сессий, определённая с заданными параметрами
    return async_sessionmaker(
        bind=bind_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


# Создание асинхронного движка SQLAlchemy для работы с PostgreSQL
engine = create_async_engine(app_settings.postgres_dsn.unicode_string())

# Создание фабрики для сессий
async_session = create_sessionmaker(engine)

# Создание зависимости для работы с базой данных
db_dependency = Annotated[AsyncSession, Depends(get_async_session)]
