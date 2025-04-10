from sqlalchemy.future import select
from fastapi import FastAPI, APIRouter, HTTPException,  Depends
from models import Document, Contract, Сontract_Documentt
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter( prefix="/api/v1/SM", tags=["SM"])
async def get_db():
    async with SessionLocal() as db:
        try: yield db  
        finally: await db.close()
@router.post("/create_order")
async def create_order(name: str, desc: str, db: AsyncSession = Depends(get_db)):
    new_order = Contract(con_name=name, description=desc)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order
@router.get("/get_order/{con_id}")
async def read_order(con_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contract).filter(Contract.con_id == con_id)) 
    contract = result.scalars().first()
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")  
    return { "con_id": contract.con_id, "con_name": contract.con_name, "description": contract.description, "create_date": contract.create_date}
@router.post("/adding_service_to_order")
async def connect_service_order(con_id: int, doc_id: int, db: AsyncSession = Depends(get_db)):
    new_connect = Сontract_Documentt(contract_id=con_id, document_id=doc_id)
    db.add(new_connect)
    await db.commit()
    await db.refresh(new_connect)
    return new_connect
@router.get("/read_service_in_order")
async def read_service_in_order(con_doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Сontract_Documentt).filter(Сontract_Documentt.con_doc_id == con_doc_id))  
    service_order = result.scalars().first()  
    result = await db.execute(select(Document).filter(Document.doc_id == service_order.document_id))
    document = result.scalars().first()
    result = await db.execute(select(Contract).filter(Contract.con_id == service_order.contract_id))
    contract = result.scalars().first()
    if service_order is None: raise HTTPException(status_code=404, detail="Contract not found")  
    return {"Документ": f"Linked to doc id {service_order.contract_id}", "file_name": document.file_name, "file_type": document.file_type, "Контракт": f"Привязан к документу c id {service_order.document_id}", "con_name": contract.con_name, "description": contract.description, "Дата привязки": service_order.date_bind}