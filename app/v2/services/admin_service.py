from typing import Any, Dict
from fastapi import HTTPException, status
from httpx import HTTPStatusError

from app.v2.models.admin import Admin, AdminData, AdminSignIn
from app.v2.services.language import fetch_languages
from app.utils.password_encript import hash_password, verify_password
from app.utils.logger import logger
from app.v2.auth.jwt_handler import sign_jwt


class AdminService:
    async def register_admin(self, admin: Admin):
        print("HEREREERERERER")
        admin_exists = await Admin.find_one(Admin.email == admin.email)
        if admin_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Admin with email supplied already exists"
            )
        try:
            admin.password = hash_password(admin.password)
            new_admin = await admin.create()
            return {"message": "Admin registered successfully", "data": new_admin.model_dump(by_alias=True)}
        except Exception as e:
            logger.error(f"Error registering admin: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to register admin: {e}"
            )

    
    async def login_admin(self, admin: AdminSignIn) -> Dict[str, str]:
        admin_exists = await Admin.find_one(Admin.email == admin.username)
        
        if not admin_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin with the provided email not found"
            )

        password_valid = verify_password(admin.password, admin_exists.password)
        
        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect email or password"
            )
        
        return sign_jwt(admin_exists.id)
