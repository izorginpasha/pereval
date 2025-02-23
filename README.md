
##Документация API доступна по адресу http://45.143.92.70:8010/api/openapi#/
## OpenAPI JSON http://45.143.92.70:8010/openapi.json
## OpenAPI YAML: Скачайте файл openapi.yaml, сохраненный при старте приложения.

### Примеры запросов
#### curl -X 'GET' \
  'http://45.143.92.70:8010/submitData/6' \
  -H 'accept: application/json'

# Приложение Pereval
---

Добро пожаловать в **Pereval** — современное REST API, построенное с использованием **FastAPI**. Этот проект позволяет быстро получать, создавать и управлять данными о состоянии горных перевалов.

---

## Оглавление

- [Установка](#установка)
- [Запуск](#запуск)
- [Документация API](#документация-api)
- [Docker-образ](#docker-образ)
- [Примеры запросов](#примеры-запросов)
- [Особенности](#особенности)
- [Контакты](#контакты)


---

## Установка

### Перед запуском убедитесь, что у вас установлены:

- python:3.11
- pip
- **Docker (если используете контейнеризацию)**
- **PostgreSQL

### Создание базы данных
- в корне приложения создаите фаил .env с пременными 
FSTR_DB_HOST=127.0.0.1 (если будете использовать готовыи докер образ то FSTR_DB_HOST=db)
FSTR_DB_PORT=5432
FSTR_DB_LOGIN=
FSTR_DB_PASS=
FSTR_DB_NAME=
- после установки выполните миграции  
alembic upgrade head

### Установка зависимостей
pip install -r requirements.txt
Запуск
src/main.py

### Документация API
- Документация API доступна по адресу http://45.143.92.70:8010/api/openapi#/
- OpenAPI JSON http://45.143.92.70:8010/openapi.json
- OpenAPI YAML: Скачайте файл openapi.yaml, сохраненный при старте приложения.

### Установка и запуск через Docker Compose
- Установите Docker и Docker Compose
Перед началом работы убедитесь, что у вас установлены:
Docker
Docker Compose (обычно идет в комплекте с Docker)

- Проверьте, что Docker и Compose установлены, выполнив команды:
docker --version
docker compose version  -- Для новой версии
docker-compose --version  -- Для старой версии
-  Запуск контейнеров
После настройки запустите контейнеры с помощью:

docker compose up -d
Флаг -d означает запуск в фоновом режиме.
Если нужно обновить контейнеры, используйте:
docker compose up --build -d
Чтобы проверить запущенные контейнеры:
docker ps
- если провоить установку на хосте можно использовать готовыи образ
для этого нужно изменить docker-compose-yaml и загрузить или создать вкорне проекта
поместить внутрь фаила
services:
  db:
    image: postgres:15
    container_name: db
    restart: always
    environment:
      POSTGRES_USER: ${FSTR_DB_LOGIN}
      POSTGRES_PASSWORD: ${FSTR_DB_PASS}
      POSTGRES_DB: ${FSTR_DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "${FSTR_DB_PORT}:5432"
    networks:
      - app_network

  app:
    image: izorginpasha/pereval-app:latest
    container_name: pereval
    restart: always
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://${FSTR_DB_LOGIN}:${FSTR_DB_PASS}@db:${FSTR_DB_PORT}/${FSTR_DB_NAME}       
    ports:
      - "8010:8010"
    networks:
      - app_network

networks:
  app_network:
    driver: bridge

далее выполнить предыдущии шаг, еще после создания контеинеров в контеинере db
выполнить сброс миграции 

docker compose exec db psql -U my_user -d my_database -c "DROP TABLE IF EXISTS alembic_version;"
docker compose exec db bash
alembic stamp head
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head


### Примеры запросов
#### curl -X 'GET' \
  'http://45.143.92.70:8010/submitData/6' \
  -H 'accept: application/json'
#### Ответ: 
{
  "id": 6,
  "date_added": "2025-02-23T09:49:03.600213",
  "beautyTitle": "string",
  "title": "string",
  "other_titles": "string",
  "connect": "string",
  "add_time": "2025-02-22T09:16:06.480000",
  "status": "new",
  "user": {
    "email": "user@example.com",
    "fam": "string",
    "name": "string",
    "otc": "string",
    "phone": "string"
  },
  "coords": {
    "latitude": 0,
    "longitude": 0,
    "height": 0
  },
  "level": {
    "level_winter": "string",
    "level_summer": "string",
    "level_autumn": "string",
    "level_spring": "string"
  },
  "images": [
    {
      "data": "https://s9.travelask.ru/uploads/post/000/028/766/main_image/facebook-3703d50448b0b279bd310d3d2ce9f03d.jpg"
    }
  ]
}
данныи запрос позволяет получить информацию о перевале по его id
#### 
#### Виды запросов
- GET http://45.143.92.70:8010/submitData/<id> для получения информации о конкретном перевале 
- GET http://45.143.92.70:8010/submitData/<email> для получения информации о всех перевалах 
добавленных пользователем с данным email
- POST http://45.143.92.70:8010/submitData/ для отпавки данных о новом перевале
- POST http://45.143.92.70:8010/submitData/<id> для изменения данных о перевале
полное описание и возможность протестировать, можно получить по ссылке http://45.143.92.70:8010/api/openapi#/

### Особенности

✅ Быстрое и легкое
Использование FastAPI позволяет создавать высокопроизводительные асинхронные API с минимальной задержкой.

✅ Асинхронность
Благодаря async/await в Python API эффективно обрабатывает множество запросов одновременно, не блокируя выполнение кода. Это особенно полезно для работы с базами данных, сетевыми запросами и внешними сервисами.

✅ Автоматическая документация
Документация OpenAPI (Swagger UI и ReDoc) генерируется автоматически, что упрощает тестирование и интеграцию API.

✅ Удобная обработка ошибок
Пользовательские сообщения об ошибках валидации помогают быстро выявлять и исправлять ошибки ввода, а кастомные обработчики исключений позволяют возвращать понятные ответы.

✅ Готовность к продакшену
FastAPI отлично работает в связке с Uvicorn (асинхронным сервером), а также поддерживает Gunicorn, Docker, NGINX и CI/CD для развертывания в продакшене.

### Контакты

Email: izorgin.pasha@yandex.ru
GitHub: github.com/izorginpasha