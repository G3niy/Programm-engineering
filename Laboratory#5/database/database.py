#imports
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
DATABASE_URL = 'postgresql+asyncpg://postgres:1234@localhost/testdb' #url to database
#postgresql+asyncpg://user:pass@localhost/base_name
engine = create_async_engine(DATABASE_URL) # создает асинхронный объект engine, который служит для подключения к базе данных.
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession) # создает класс сессии SessionLocal, который будет использоваться для работы с базой данных.
Base = declarative_base() # создает базовый класс для всех моделей.
#наследование всех классов таблиц моделей.
import os
from motor.motor_asyncio import AsyncIOMotorClient
MONGO_URL = "mongodb://mongodb:27017"
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "project_db")
client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
async def get_services_mongo():
    return db["services"]


