from jose import JWTError, jwt
from datetime import datetime, timedelta
SECRET_KEY = "cpy0zrZvAdhQM_bQqrT8H5iIRvjWotHWwvCsl2IzXxo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
async def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError: return None