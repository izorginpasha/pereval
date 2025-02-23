import uvicorn
from core.config import uvicorn_options
from fastapi import APIRouter, FastAPI, HTTPException, Request
from sqlalchemy import text
from api import api_router
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
import yaml

logger = logging.getLogger("root")

app = FastAPI(
    docs_url="/api/openapi"
)


@app.on_event("startup")
async def save_openapi_yaml():
    with open("openapi.yaml", "w") as f:
        yaml.dump(app.openapi(), f, default_flow_style=False, allow_unicode=True)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Ошибка валидации: {exc}")
    return JSONResponse(
        status_code=400,  # Меняем стандартный 422 на 400
        content={"state": 0, "message": "Ошибка валидации JSON",
                 "detail": "Некорректные данные. Проверьте ввод и повторите попытку."}
    )


app.include_router(api_router)

if __name__ == '__main__':
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
