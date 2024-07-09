import asyncio
from typing import Sequence, Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession, AsyncScalarResult
from sqlalchemy import select, Row, RowMapping

from src.models.base_models import Discipline
from src.database import async_session, Base


def db_action(func):
    async def wrapper(obj, **kwargs):
        async with async_session() as session:
            async with session.begin():
                return await func(session, obj, **kwargs)
    return wrapper


@db_action
async def create_object(
        session: AsyncSession,
        obj: Base,
) -> Base:
    """
    Создание
    :param session:
    :param obj:
    :return: Base
    """
    try:
        session.add(obj)
    except Exception as _:
        await session.rollback()
    return obj


@db_action
async def get_objects(
        session: AsyncSession,
        obj: Base,
        **kwargs
):
    """
    Получение данных из БД

    :param kwargs: Параметры для фильрации списка объектов
    :param obj: Объект модели
    """
    result = await session.execute(select(obj).filter_by(**kwargs))
    db_objects = result.scalars().all()
    return db_objects


