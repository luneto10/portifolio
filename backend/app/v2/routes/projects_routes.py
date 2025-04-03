from fastapi import APIRouter, HTTPException, Depends
from app.v2.services.project_service import ProjectService
from app.v2.models.project import Project, ProjectCreate, ProjectGet, ProjectUpdate
from app.utils.validators import PyObjectId
from app.v2.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_project_service() -> ProjectService:
    return ProjectService()

@router.get("/", status_code=200, response_model=list[ProjectGet])
async def get_projects(service: ProjectService = Depends(get_project_service)):
    return await service.get_projects()

@router.get("/{id}", status_code=200, response_model=ProjectGet)
async def get_project_by_id(
    id: PyObjectId, service: ProjectService = Depends(get_project_service), user_id: str = Depends(get_current_user)
):
    return await service.get_project_by_id(id, user_id)

@router.post("/", status_code=201, response_model=ProjectGet)
async def insert_project(
    project: ProjectCreate, service: ProjectService = Depends(get_project_service)
):
    return await service.insert_project(project)

@router.put("/{id}", status_code=201)
async def update_project(
    id: PyObjectId,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    return await service.update_project(id, project)

@router.delete("/", status_code=200)
async def delete_projects(service: ProjectService = Depends(get_project_service)):
    return await service.delete_projects()

@router.delete("/{id}", status_code=200)
async def delete_project(
    id: PyObjectId, service: ProjectService = Depends(get_project_service)
):
    return await service.delete_project(id)
