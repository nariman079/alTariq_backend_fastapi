import logging
from typing import Annotated

import sqlalchemy
from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, UploadFile, HTTPException, Body
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.base_models import Discipline, Teacher
from src.schemas.base_schemas import DisciplineBaseSchema, TeacherBaseSchema, TeacherUpdateSchema

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


@base_router.post('/v1/admin/teachers/')
async def create_teacher_admin_handler(
        new_teacher: TeacherBaseSchema,
        db: AsyncSession = Depends(get_db)
):
    """Создание учителя в админке"""
    teacher = Teacher(**new_teacher.dict())
    db.add(teacher)
    try:
        await db.commit()
        await db.refresh(teacher)
    except sqlalchemy.exc.IntegrityError as error:
        await db.rollback()
        logging.error(msg='\n'.join(error.args))
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "Такой пользователь уже существует",
                "data": {
                    "telegram_id": teacher.telegram_id,
                    "email": teacher.email
                }
            },
        )
    except Exception as _:
        await db.rollback()
        logging.error(msg='\n'.join(_.args))
        raise HTTPException(
            status_code=500,
            detail="Неизвестная ошибка при создании учителя",
        )
    return teacher


@base_router.get('/v1/admin/disciplines/')
async def get_discipline_admin_handler(
        db: AsyncSession = Depends(get_db)
):
    """Получение списка дисциплин в админке"""

    query = await db.execute(
        select(
            Discipline
        )
    )
    try:
        disciplines = query.scalars().all()
        return disciplines
    except Exception as error:
        await db.rollback()
        logging.error(msg='\n'.join(error.args))
        raise HTTPException(
            status_code=500,
            detail="Неизвестная ошибка при получении дисциплин\nОбратитесь в поддержку altariq@info.ru",
        )


@base_router.get('/v1/admin/teachers/')
async def get_teacher_admin_handler(
        db: AsyncSession = Depends(get_db)
):
    """Получение списка учителей в админке"""
    query = await db.execute(
        select(
            Teacher
        )
    )
    try:
        teachers = query.scalars().all()
        return teachers
    except Exception as error:
        await db.rollback()
        logging.error(msg='\n'.join(error.args))
        raise HTTPException(
            status_code=500,
            detail="Неизвестная ошибка при получении дисциплин\n"
                   "Обратитесь в поддержку altariq@info.ru",
        )


@base_router.put('/v1/admin/teachers/{teacher_id}')
async def update_teacher_admin_handler(
        teacher_id: int,
        teacher: Annotated[TeacherUpdateSchema, Body()],
        db: AsyncSession = Depends(get_db)
):
    """Обновление данных  учителя в админке"""
    try:
        query = await db.execute(
            select(
                Teacher
            )
            .where(
                Teacher.id == teacher_id
            )
        )
        teacher_obj = query.scalar()

        if not teacher_obj:
            raise HTTPException(
                status_code=404,
                detail="Такой преподаватель не найден"
            )

        await db.execute(
            update(
                Teacher
            )
            .where(
                Teacher.id == teacher_id
            )
            .values(
                teacher.dict(exclude_unset=True)
            )
        )
        await db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        await db.rollback()
        logging.error(msg='\n'.join(error.args))
        raise HTTPException(
            status_code=400,
            detail={
                "msg": "Такой пользователь уже существует",
                "data": {
                    "telegram_id": teacher.telegram_id,
                    "email": teacher.email
                }
            },
        )



@base_router.patch('/v1/admin/teachers/{teacher_id}/image/')
async def update_teacher_image_admin_handler(
        teacher_id: int,
        image_file: UploadFile,
):
    """Получение списка дисциплин в админке"""

