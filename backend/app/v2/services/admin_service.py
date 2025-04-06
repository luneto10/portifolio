from typing import Any, Dict
from fastapi import HTTPException, status

from app.v2.models.admin import Admin, AdminData, AdminSignIn
from app.utils.password_encrypt import hash_password, verify_password
from app.utils.logger import logger
from app.v2.auth.jwt_handler import sign_jwt


class AdminService:
    async def register_admin(self, admin: Admin):
        admin_exists = await Admin.find_one(Admin.email == admin.email)
        if admin_exists:
            logger.error("Admin with email supplied already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Admin with email supplied already exists"
            )
        
        admin.password = hash_password(admin.password)
        new_admin = await admin.create()
        logger.info("Admin registered successfully" + str(new_admin.model_dump(mode="python")))
        return {"message": "Admin registered successfully", "data": new_admin.model_dump(by_alias=True)}
        

    
    async def login_admin(self, admin: AdminSignIn) -> Dict[str, str]:
        admin_exists = await Admin.find_one(Admin.email == admin.username)

        password_valid = verify_password(admin.password, admin_exists.password)
        
        if not password_valid or not admin_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect email or password"
            )
        
        return sign_jwt(admin_exists.id)
