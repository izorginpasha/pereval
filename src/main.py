
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

app.include_router(api_router)

if __name__ == '__main__':
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
