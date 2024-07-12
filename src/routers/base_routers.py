from fastapi import APIRouter

from src.services.base_services import create_object
from src.models.base_models import Discipline
from src.schemas.base_schemas import CreateDisciplineSchema

base_router = APIRouter()

@base_router.post('/disciplines')
async def create_discipline_handler(
        new_discipline: CreateDisciplineSchema
):
    obj = await create_object(
        obj=Discipline(**new_discipline.dict())
    )
    return obj.__dict__

