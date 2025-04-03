from typing import Any, Dict
from fastapi import APIRouter, Body, Depends

from app.v2.models.admin import Admin, AdminData, AdminSignIn
from app.v2.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_admin_service() -> AdminService:
    return AdminService()
@router.post("/register", status_code=201, response_model=Dict[str, Any])
async def register_admin(admin: Admin = Body(...), service: AdminService = Depends(get_admin_service)):
    return await service.register_admin(admin)

@router.post("/login", status_code=200, response_model=Dict[str, str])
async def login_admin(admin: AdminSignIn = Body(...), service: AdminService = Depends(get_admin_service)):
    return await service.login_admin(admin)


