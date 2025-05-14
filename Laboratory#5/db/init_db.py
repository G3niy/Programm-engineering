import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from database import Base, engine
from models import User, Orders, Services

async def create_test_data(session: AsyncSession):
    users = [
        User(
            first_name="Геннадий",
            last_name="Грушецкий",
            username="geniy",
            email="geniy@example.com",
            password_hashed="hashed_password_1"
        ),
        User(
            first_name="Кириллов",
            last_name="Андрей",
            username="kirill",
            email="kirill@example.com",
            password_hashed="hashed_password_2"
        ),
    ]
    
    session.add_all(users)
    await session.flush()     

    orders = [
        Orders(
            name="Засор водопроводной системы",
            description="Засорилась выводная труба в квартире на шестом этаже"
        ),
    ]
    
    session.add_all(orders)
    await session.flush()
    
    services = [
        Services(
            code="Water-6",
            title="Засор",
            description="Выбрать крота и приехать на место с диагностикой",
            project_id=Orders[0].id,
            user_id=users[0].id
        ),
    ]
    
    session.add_all(services)
    await session.commit()
    
    print("Созданы тестовые данные:")
    print(f"- Пользователей: {len(users)}")
    print(f"- Заказов: {len(orders)}")
    print(f"- Услуг: {len(services)}")

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    
    async with async_session() as session:
        await create_test_data(session)

if __name__ == "__main__":
    asyncio.run(create_all())