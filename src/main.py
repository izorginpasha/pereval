import uvicorn
from core.config import uvicorn_options
from fastapi import APIRouter, FastAPI, HTTPException, Request
from sqlalchemy import text
from api import api_router
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("root")

app = FastAPI(
    docs_url="/api/openapi"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Ошибка валидации: {exc}")
    return JSONResponse(
        status_code=400,  # Меняем стандартный 422 на 400
        content={"state": 0, "message": "Ошибка валидации JSON", "detail": "Некорректные данные. Проверьте ввод и повторите попытку."}
    )


app.include_router(api_router)

if __name__ == '__main__':
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
