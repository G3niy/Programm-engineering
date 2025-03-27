from sqlalchemy.future import select
from fastapi import FastAPI, APIRouter, HTTPException,  Depends, status
#from models import Document, Contract, Сontract_Documentt
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter( prefix="/api/v1/OrdersAndServices", tags=["OrdersAndServices"])
#async def get_db():
    #async with SessionLocal() as db:
        #try: yield db  
        #finally: await db.close()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
db_services = []
db_orders = [[]]
users_db = []
@router.post("/create_service")
async def create_service(name: str, desc: str):
    new_service = input("name of service:", str())
    db_services.append(new_service)
    return new_service
    #db.add(new_contract)
    #await db.commit()
    #await db.refresh(new_contract)
    #return new_contract

@router.get("/get_services")
async def get_services(db_services):
    for i in db_services:
        print(i)
    return {"orders_list"}

@router.post("/add_service_to_order")
async def add_service(name: str):
    for i in db_services:
        if i == name:
            db_orders.append(i)
    return db_orders


@router.get("/get_user_order")
async def get_user_order(db_orders, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username in users_db:
            return db_orders[0]
        else:
            return str('user_not_found')
    except JWTError:
        raise credentials_exception
