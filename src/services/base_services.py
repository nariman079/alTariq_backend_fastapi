import asyncio
import logging
from typing import Sequence, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, delete, update

from src.models.base_models import Discipline
from src.database import async_session, Base

logging.basicConfig(filename='myapp.log', level=logging.ERROR)


def db_action(func):
    """ Декоратор """

    async def wrapper(obj, **kwargs):
        try:
            async with async_session() as session:
                async with session.begin():
                    return await func(session, obj, **kwargs)
        except Exception as error:
            logging.log(
                level=logging.ERROR,
                msg="\n".join(error.args)
            )

    return wrapper


@db_action
async def create_object(
        session: AsyncSession,
        obj: Any,
) -> Any:
    """
    Создание объекта в БД
    """
    session.add(obj)
    return obj


@db_action
async def get_object(
        session: AsyncSession,
        obj: Base,
        obj_id: int,
):
    """
    Получение объекта из БД по его ID
    """
    result: Result = await session.execute(
        select(
            obj
        )
        .where(
            obj.id == obj_id
        )
    )
    response_obj = result.scalars().first()
    return response_obj


@db_action
async def get_objects(
        session: AsyncSession,
        obj: Base,
        **kwargs
) -> Sequence[Any]:
    """
    Получение объектов из БД
    """
    result = await session.execute(select(obj).filter_by(**kwargs))
    db_objects = result.scalars().all()
    return db_objects


@db_action
async def update_object(
        session: AsyncSession,
        obj: Base,
        obj_id: int,
        update_data: dict
):
    update_stmt = update(
            obj
        ).where(
            obj.id == obj_id
        ).values(
            **update_data
        )
    await session.execute(
        update_stmt
    )
    return None

@db_action
async def update_objects(
        session: AsyncSession,
        obj: Base,
        obj_ids: List[int],
        update_data: dict
):
    update_stmt = update(
            obj
        ).where(
            obj.id.in_(obj_ids)
        ).values(
            **update_data
        )
    await session.execute(
        update_stmt
    )
    return len(obj_ids)


@db_action
async def delete_objects(
        session: AsyncSession,
        obj: Base,
        obj_ids: List[int]

) -> int:
    """
    Удаление списка объектов из БД
    """
    await session.execute(
        delete(obj).where(
            obj.id.in_(obj_ids)
        )
    )
    return len(obj_ids)


@db_action
async def delete_object(
        session: AsyncSession,
        obj: Base,
        obj_id: List[int]

) -> None:
    """
    Удаление списка объектов из БД
    """
    await session.execute(
        delete(obj).where(
            obj.id.in_(obj_id)
        )
    )
    return None


