from datetime import datetime, timedelta, timezone
import time
from typing import Dict

from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError

from app.v2.core.config import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def token_response(token: str):
    return {"access_token": token}


SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = Settings().ALGORITHM  
EXPIRATION_TIME_MINUTES = 30

def sign_jwt(admin_id: ObjectId) -> str:
    payload = {
        "sub": str(admin_id), 
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    try:
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token_response(token)
    except Exception as e:
        raise Exception(f"Error signing JWT: {e}")

def verify_jwt(jwtoken: str) -> bool:
    isTokenValid: bool = False

    payload = decode_jwt(jwtoken)
    if payload:
        isTokenValid = True
    return isTokenValid

def decode_jwt(token: str) -> dict:
    """
    Decode the JWT token and verify its expiration.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        return decoded_token
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_current_user(token: str = Depends(oauth2_scheme)) :
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = id
    except JWTError:
        raise credentials_exception
    return token_data
