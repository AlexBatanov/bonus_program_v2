from os import getenv
import asyncio

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


load_dotenv()

engine = create_async_engine(getenv("DB_URL"), echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

