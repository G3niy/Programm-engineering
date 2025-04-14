from sqlalchemy.future import select
from fastapi import FastAPI, APIRouter, HTTPException,  Depends
from models.models import Services, Orders
from sqlalchemy.orm import Session
from database.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter( prefix="/api/v1/SM", tags=["SM"])
import uvicorn

app = FastAPI()
async def get_db():
    async with SessionLocal() as db:
        try: yield db  
        finally: await db.close()
@app.post("/create_order")
async def create_order(name: str, desc: str, db: AsyncSession = Depends(get_db)):
    new_order = Services(con_name=name, description=desc)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order
@app.get("/get_order/{con_id}")
async def read_order(con_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Services).filter(Services.con_id == con_id)) 
    Services = result.scalars().first()
    if Services is None:
        raise HTTPException(status_code=404, detail="Services not found")  
    return { "con_id": Services.con_id, "con_name": Services.con_name, "description": Services.description, "create_date": Services.create_date}
@app.post("/adding_service_to_order")
async def connect_service_order(con_id: int, doc_id: int, db: AsyncSession = Depends(get_db)):
    new_connect = Orders(Services_id=con_id, Orders_id=doc_id)
    db.add(new_connect)
    await db.commit()
    await db.refresh(new_connect)
    return new_connect
@app.get("/read_service_in_order")
async def read_service_in_order(con_doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Orders).filter(Orders.con_doc_id == con_doc_id))  
    service_order = result.scalars().first()  
    result = await db.execute(select(Orders).filter(Orders.doc_id == service_order.Orders_id))
    Orders = result.scalars().first()
    result = await db.execute(select(Services).filter(Services.con_id == service_order.Services_id))
    Services = result.scalars().first()
    if service_order is None: raise HTTPException(status_code=404, detail="Services not found")  
    return {"Услуга в заказе": f"Linked to doc id {service_order.Services_id}", "file_name": Orders.file_name, "file_type": Orders.file_type, "Контракт": f"Привязан к документу c id {service_order.Orders_id}", "con_name": Services.con_name, "description": Services.description, "Дата привязки": service_order.date_bind}


if __name__ == "__main__":
    uvicorn.run("orders.Orders:app", reload=True)