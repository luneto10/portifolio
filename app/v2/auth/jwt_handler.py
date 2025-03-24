from datetime import datetime, timedelta, timezone
import time
from typing import Dict

from bson import ObjectId
from fastapi import HTTPException
import jwt

from app.v2.core.config import Settings

def token_response(token: str):
    return {"access_token": token}


secret_key = Settings().SECRET_KEY
algorithm = Settings().ALGORITHM  


def sign_jwt(admin_id: ObjectId) -> str:
    payload = {
        "sub": str(admin_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    try:
        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        return token_response(token)
    except Exception as e:
        raise Exception(f"Error signing JWT: {e}")


def decode_jwt(token: str) -> dict:
    """
    Decode the JWT token and verify its expiration.
    """
    try:
        # Decode the JWT and verify expiration
        decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm], options={"verify_exp": True})
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
