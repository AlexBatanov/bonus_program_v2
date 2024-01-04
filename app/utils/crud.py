from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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