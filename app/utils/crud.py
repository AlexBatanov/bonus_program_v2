from sqlalchemy import select
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


async def get_all_obj(async_session: AsyncSession, model, attr, param):
    async with async_session() as session:
        db_obj = await session.execute(
            select(model).filter(getattr(model, attr) == param))
        return db_obj.scalars()


async def update_obj(async_session: AsyncSession, obj):
    async with async_session() as session:
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