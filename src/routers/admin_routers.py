import logging

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.base_models import Discipline
from src.schemas.base_schemas import DisciplineBaseSchema, TeacherBaseSchema

base_router = APIRouter()


@base_router.post('/v1/admin/disciplines/')
async def create_discipline_admin_handler(
        new_discipline: DisciplineBaseSchema,
        db: AsyncSession = Depends(get_db)
):
    """Создание дисциплины в админке"""
    discipline = Discipline(**new_discipline.dict())
    db.add(discipline)
    try:
        await db.commit()
        await db.refresh(discipline)
    except Exception as _:
        await db.rollback()
        logging.error(msg='\n'.join(_.args))
        raise HTTPException(
            status_code=500,
            detail="Ошибка при создании дисциплины",
        )
    return discipline


@base_router.post('v1/admin/teachers/')
async def create_teacher_admin_handler(
        new_teacher: TeacherBaseSchema
):
    """Создание учителя в админке"""
    ...


@base_router.get('/v1/admin/disciplines/')
async def get_discipline_admin_handler():
    """Получение списка дисциплин в админке"""
    ...


@base_router.get('v1/admin/teachers/')
async def get_teacher_admin_handler():
    """Получение списка учителей в админке"""
    ...


@base_router.put('v1/admin/teachers/{teacher_id}')
async def update_teacher_admin_handler(
        teacher_id: int,
        teacher: TeacherBaseSchema
):
    """Получение списка учителей в админке"""
    ...


@base_router.patch('/v1/admin/teachers/{teacher_id}/image/')
async def update_teacher_image_admin_handler(
        teacher_id: int,
        image_file: UploadFile,
):
    """Получение списка дисциплин в админке"""
    ...
