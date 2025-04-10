from auth.hash_password import get_password_hash
from sqlalchemy.future import select
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from fastapi.security import OAuth2PasswordBearer
from models import User
from sqlalchemy.orm import defer
from database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from auth.jwt_token import decode_token
from typing import Optional, List
router = APIRouter(
    prefix="/api/v1/user", 
    tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")



async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

@router.get("/Search_login/{user_login}")
async def get_user_login(user_login: str,
                       token: str = Depends(oauth2_scheme),
                       db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == user_login))
    user = result.scalars().first()
  
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user

@router.get("/Search_mask/")
async def get_user_mask(
    first_name: Optional[str] = Query(None, min_length=1, description="Маска для поиска по имени"),
    last_name: Optional[str] = Query(None, min_length=1, description="Маска для поиска по фамилии"),
    db: AsyncSession = Depends(get_db)
):
    """
    Поиск пользователей по маске имени и/или фамилии.
    Возвращает список пользователей, у которых имя или фамилия содержат указанные строки.
    """
    query = select(User)
    
    if first_name:
        query = query.filter(User.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(User.last_name.ilike(f"%{last_name}%"))
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    return {
        "count": len(users),
        "users": [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email
            }
            for user in users
        ]
    }

@router.put("/update_user/{user_id}")
async def update_user(
    user_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Обновление информации о пользователе
    
    Параметры:
    - user_id: ID пользователя для обновления
    - first_name: Новое имя (опционально)
    - last_name: Новая фамилия (опционально)
    - email: Новый email (опционально)
    - password: Новый пароль (опционально)
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Обновляем только те поля, которые переданы
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        # Проверяем, что новый email не занят другим пользователем
        existing_email = await db.execute(
            select(User).filter(
                User.email == email,
                User.id != user_id
            )
        )
        if existing_email.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже используется другим пользователем"
            )
        user.email = email
    if password is not None:
        user.password_hashed = await get_password_hash(password)
    
    await db.commit()
    await db.refresh(user)
    
    return {"message": "Пользователь успешно обновлен"}

@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Удаление пользователя
    """
    result = await db.execute(
        select(User).filter(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    await db.delete(user)
    await db.commit()
    
    return {"message": "Пользователь успешно удален"}