from datetime import date

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def create_obj(async_session: AsyncSession, obj):
    async with async_session() as session:
        session.add(obj)
        await session.commit()


async def get_obj(async_session: AsyncSession, model, attr, param):
    async with async_session() as session:
        db_obj = await session.execute(
            select(model).filter(getattr(model, attr) == param))
        return db_obj.scalar()


# async def get_all_obj(async_session: AsyncSession, model, attr, param):
#     async with async_session() as session:
#         db_obj = await session.execute(
#             select(model).filter(getattr(model, attr) == param))
#         return db_obj.scalars()


async def update_obj(async_session: AsyncSession, obj):
    async with async_session() as session:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)


async def added_obj_in_array_and_update(async_session: AsyncSession, obj, data):
    async with async_session() as session:
        employee = obj.warranty_employee
        employee.append('skd')
        print(employee)
        obj.warranty_employee = employee
        session.add(obj)
        await session.commit()
        await session.refresh(obj)


async def get_obj_relation(async_session: AsyncSession, model, attr, param, attr_relation):
    async with async_session() as session:
        db_obj = await session.execute(
            select(model).filter(getattr(model, attr) == param).options(
                selectinload(getattr(model, attr_relation))
            )
        )
        return db_obj.scalar()


async def get_all_obj(async_session: AsyncSession, model):
    """Получение всех объектов"""
    async with async_session() as session:
        db_objects = await session.execute(
            select(model)
        )
        return db_objects.scalars().all()


async def get_objects_today(async_session: AsyncSession, model, attr):
    """Получение объектов за текущую дату"""
    now_day = date.today()
    async with async_session() as session:
        db_objects = await session.execute(
            select(model).filter(func.date(getattr(model, attr)) == now_day)
        )
        return db_objects.scalars().all()


async def get_obj_by_id(async_session: AsyncSession, model, id):
    """Получение объекта по id"""
    async with async_session() as session:
        obj = await session.get_one(model, id)
        return obj


async def get_objects_by_date(async_session: AsyncSession, model, attr, start, end):
    """Получаем объекты фильтрованные по периоду дат"""
    async with async_session() as session:
        objects = await session.execute(select(model).\
                  filter(getattr(model, attr).between(start, end)))
        return objects.scalars().all()