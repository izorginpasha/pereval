from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.pereval import PerevalCreate, ResponseMessage, User, Image, Coord, Level, PerevalResponse
from services.crud_pereval import create_pereval, get_pereval
from db.db import db_dependency

pereval_router = APIRouter(prefix="/submitData", tags=['submitData'])


@pereval_router.post("/", response_model=ResponseMessage)
async def submit_data(pereval: PerevalCreate, db: db_dependency):
    result = await create_pereval(db, pereval)
    return result
@pereval_router.get("/{pereval_id}", response_model=PerevalResponse)
async def read_pereval(db: db_dependency, pereval_id: int):
    result = await get_pereval(db, pereval_id)
    return result