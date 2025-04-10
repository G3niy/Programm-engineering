from sqlalchemy.future import select
from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, Depends
from fastapi.security import OAuth2PasswordBearer
from models import Document, User
from sqlalchemy.orm import Session, defer
from database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from authentication.token_creation import decode_token
router = APIRouter(prefix="/api/v1/ABS", tags=["ABS"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
async def get_db():
    async with SessionLocal() as db:
        try: yield db
        finally: await db.close()
@router.get("/all_services")
async def get_all_services(db: AsyncSession = Depends(get_db)):
    query = select(Document).options(defer(Document.file_data))
    documents = (await db.execute(query)).scalars().all()
    if documents is None: raise HTTPException(status_code=404, detail="Document not found")
    return {"services_list": documents}
@router.get("/service_finder/{doc_id}")
async def get_service(doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).filter(Document.doc_id == doc_id))
    document = result.scalars().first()
    if document is None: raise HTTPException(status_code=404, detail="Document not found")
    return {"service_id": document.doc_id, "service_name": document.file_name, "service_type": document.file_type, "creation_date": document.upload_date, "user_id": document.user_id, "name": document.user_id }
@router.get("/client_services/")
async def clients_services(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
    if payload is None: raise HTTPException(status_code=401, detail="Неверный токен или срок действия истёк")
    if payload["sub"] is None: raise HTTPException(status_code=401, detail="Пользователь не найден в токене")
    id_user = await db.execute(select(User).filter(User.username == payload["sub"]))
    id_user = id_user.scalars().first().id
    query = select(Document).filter(Document.user_id == id_user)
    query = query.options(defer(Document.file_data))
    documents = (await db.execute(query)).scalars().all()
    if documents is None: raise HTTPException(status_code=404, detail="Document not found")
    return {"contract_list": documents}