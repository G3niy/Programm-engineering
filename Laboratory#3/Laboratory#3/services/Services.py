from sqlalchemy.future import select
from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, Depends
from fastapi.security import OAuth2PasswordBearer
from models.models import Services, User
from sqlalchemy.orm import Session, defer
from database.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from authentication.token_creation import decode_token
router = APIRouter(prefix="/api/v1/ABS", tags=["ABS"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
import uvicorn
app = FastAPI()
async def get_db():
    async with SessionLocal() as db:
        try: yield db
        finally: await db.close()
@app.get("/all_services")
async def get_all_services(db: AsyncSession = Depends(get_db)):
    query = select(Services).options(defer(Services.file_data))
    Servicess = (await db.execute(query)).scalars().all()
    if Servicess is None: raise HTTPException(status_code=404, detail="Services not found")
    return {"services_list": Servicess}
@app.get("/service_finder/{doc_id}")
async def get_service(doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Services).filter(Services.doc_id == doc_id))
    Services = result.scalars().first()
    if Services is None: raise HTTPException(status_code=404, detail="Services not found")
    return {"service_id": Services.doc_id, "service_name": Services.file_name, "service_type": Services.file_type, "creation_date": Services.upload_date, "user_id": Services.user_id, "name": Services.user_id }
@app.get("/client_services/")
async def clients_services(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = await decode_token(token)
    if payload is None: raise HTTPException(status_code=401, detail="Неверный токен или срок действия истёк")
    if payload["sub"] is None: raise HTTPException(status_code=401, detail="Пользователь не найден в токене")
    id_user = await db.execute(select(User).filter(User.username == payload["sub"]))
    id_user = id_user.scalars().first().id
    query = select(Services).filter(Services.user_id == id_user)
    query = query.options(defer(Services.file_data))
    Servicess = (await db.execute(query)).scalars().all()
    if Servicess is None: raise HTTPException(status_code=404, detail="Services not found")
    return {"contract_list": Servicess}

if __name__ == "__main__":
    uvicorn.run("services.Services:app", reload=True)