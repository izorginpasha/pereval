
import uvicorn
from src.core.config import uvicorn_options
from fastapi import APIRouter, FastAPI, HTTPException, Request
from sqlalchemy import text
from src.api import api_router
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse




app = FastAPI(
    docs_url="/api/openapi"
)
# Глобальный обработчик ошибок валидации (422 Unprocessable Entity)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,  # Меняем стандартный 422 на 400
        content={"detail": "Некорректные данные. Проверьте ввод и повторите попытку."}
    )

# Глобальный обработчик любых других исключений
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"detail": "Произошла ошибка. Проверьте ввод и повторите попытку."}
    )
app.include_router(api_router)

if __name__ == '__main__':
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
