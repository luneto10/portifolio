# app/v2/repositories/admin_repository.py
from typing import Optional
from app.v2.models.admin import Admin

class AdminRepository:
    async def find_admin_by_email(self, email: str) -> Optional[Admin]:
        raise NotImplementedError()

    async def create_admin(self, admin: Admin) -> Admin:
        raise NotImplementedError()
