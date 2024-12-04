from jose import jwt, JWTError
from datetime import datetime, timedelta
import app.schemas as schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

secret_key = os.getenv("SECRET_KEY")
algorithm = "HS256"
access_token_expire_minute = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minute)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return token

def verify_access_token(token: str, credentails_exception):

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        id:str = payload.get("user_id")

        if id is None:
            raise credentails_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentails_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentails_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentails_exception)