import asyncio
import logging
import re
from typing import Sequence, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, delete, update

from src.models.base_models import Discipline, Image
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


# async def main():
#     # new_discipline: Discipline = await create_object(
#     #     obj=Discipline(
#     #         title="Маджвид",
#     #         priority=12
#     #     )
#     # )
#     # discipline: Discipline = await get_object(
#     #     obj=Discipline,
#     #     obj_id=new_discipline.id-1
#     # )
#     # print(discipline.title)
#     # update_discipline = await update_object(
#     #     obj=Discipline,
#     #     obj_id=discipline.id,
#     #     update_data=dict(
#     #         title="Test Title"
#     #     )
#     # )
#     # obj_ids_for_delete = [discipline.id, discipline.id - 1]
#     #
#     # print(obj_ids_for_delete)
#     #
#     # deleted_objects = await delete_objects(
#     #     obj=Discipline,
#     #     obj_ids=obj_ids_for_delete
#     # )
#     #
#     # print(deleted_objects)
#     pass

#
# @db_action
# async def d(
#         session: AsyncSession,
#         obj: Base
# ):
#     ds = await session.execute(select(obj))
#     print(ds.scalars().all())
# async def main():
#     await d(obj=Image)
#
# if __name__ == '__main__':
#     asyncio.run(main())
#
#
# from pypdf import PdfReader
#
#
# # reads table from pdf file
#
# def is_valid_format(input_string):
#     pattern = r'^\d{1,3} \d{1,3}-\d{1,3}-\d{1,3} \d{1,3}$'
#     return bool(re.match(pattern, input_string))
#
#
# def is_slip_format(input_string: str):
#     pattern = r'^\d{1,4}-\d{1,3}-\d{1,3} \d{1,3}$'
#     return bool(re.match(pattern, input_string))
#
#
# d = PdfReader("/home/nariman079i/Downloads/DSD.pdf")
# all_snils = set()
# all_str = []
# all_s = []
# for i in d.pages:
#     all_str.extend(i.extract_text().split('\n'))
#
# for i in all_str:
#     if is_valid_format(i):
#         d = i.split(' ')[1]
#         s = d + " " + i.split(' ')[-1]
#         all_snils.add(s)
#         all_s.append(s)
#     elif is_slip_format(i):
#         d = i.split(' ')[0]
#         s = d[1:] + " " + i.split(' ')[-1]
#         all_s.append(s)
#         all_snils.add(s)
#
# print(len(all_s), len(all_snils))

# unique_ids = set()
#
# with open('/home/nariman079i/Downloads/test2.csv', 'r') as f:
#     for row in f.readlines():
#         id_ = row.split(',')[0]
#         count = row.split(',')[1]
#         unique_ids.add(row)
#         # unique_ids.add({
#         #     'id': id_,
#         #     'count': count
#         # })
#
# result_data = list()
#
# for i in list(unique_ids):
#     id_ = i.split(',')[0]
#     count = i.split(',')[1]
#     result_data.append(
#         {
#             'id': id_,
#             'count': count
#         }
#     )
# for i, v in enumerate(reversed(sorted(result_data, key=lambda x: x['count']))):
#     print(i, v)