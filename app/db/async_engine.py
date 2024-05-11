import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")

load_dotenv()

db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_async_engine(db_url, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
