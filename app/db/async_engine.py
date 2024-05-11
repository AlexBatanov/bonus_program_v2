import os
import time

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")

load_dotenv()

db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}"


def connect_to_database(db_url, max_retries=10, retry_interval=1):
    retry_count = 0
    connected = False
    engine = None

    while not connected and retry_count < max_retries:
        try:
            engine = create_async_engine(db_url, echo=True)
            connection = engine.connect()
            connection.close()
            connected = True
            print("Connected to database")
        except Exception as e:
            print(f"Filed to connection to the database {e}")
            retry_count += 1
            time.sleep(retry_interval)

engine = connect_to_database(db_url)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
