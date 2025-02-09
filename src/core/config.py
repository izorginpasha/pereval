import multiprocessing
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from pydantic import Field  # Импортируем Field
import logging
import os
from dotenv import load_dotenv
from pydantic_core import MultiHostUrl

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
load_dotenv()


class AppSettings(BaseSettings):
    app_port: int = 8000
    app_host: str = "localhost"
    reload: bool = True
    cpu_count: int | None = None

    # Подключение к БД через переменные окружения
    db_host: str = os.getenv("FSTR_DB_HOST")
    db_port: int = os.getenv("FSTR_DB_PORT")
    db_user: str = os.getenv("FSTR_DB_LOGIN")
    db_password: str = os.getenv("FSTR_DB_PASS")
    db_name: str = os.getenv("FSTR_DB_NAME")


    @property
    def postgres_dsn(self) -> PostgresDsn:
        dsn = f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return PostgresDsn(dsn)

    jwt_secret: str = "your_super_secret"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"  # Файл с переменными окружения
        env_file_encoding = "utf-8"
        extra = "allow"  # Разрешаем дополнительные переменные


# Загружаем настройки
try:
    app_settings = AppSettings()
except Exception as e:
    logging.error(f"Ошибка загрузки конфигурации: {e}")
    raise

# Набор опций для запуска сервера
uvicorn_options = {
    "host": app_settings.app_host,
    "port": app_settings.app_port,
    "workers": app_settings.cpu_count or multiprocessing.cpu_count(),
    "reload": app_settings.reload
}

# Логируем настройки (без секрета и пароля)
logging.info(f"Запуск на {app_settings.app_host}:{app_settings.app_port}")
logging.info(f"Подключение к БД: {app_settings.db_host}:{app_settings.db_port}/{app_settings.db_name}")
