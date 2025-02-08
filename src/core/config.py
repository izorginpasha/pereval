import multiprocessing
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
import logging

class AppSettings(BaseSettings):
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: int | None = None

    # Подключение к БД через переменные окружения
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    # Формируем DSN для PostgreSQL
    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    jwt_secret: str = "your_super_secret"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"  # Файл с переменными окружения
        extra = "allow"  # Разрешаем дополнительные переменные

app_settings = AppSettings()

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
