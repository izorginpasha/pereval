# Импортируем FastAPI для создания веб-приложения
import uvicorn
from src.core.config import uvicorn_options
from fastapi import APIRouter, FastAPI
from sqlalchemy import text
from db.db import db_dependency

router = APIRouter()


# экземпляр роутера - метод - путь
@router.get("/path")
def my_get_func():
    pass


@router.get('/ping')
async def ping(db: db_dependency):
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


@router.post("/path")
def my_post_func():
    pass


@router.put("/path")
def my_put_func():
    pass


@router.delete("/path")
def my_delete_func():
    pass


app = FastAPI(
    docs_url="/api/openapi"
)

app.include_router(router)

if __name__ == '__main__':
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
