from fastapi import APIRouter, HTTPException, Depends
from app.services.project_service import ProjectService
from app.models.schemas.project import ProjectCreate

router = APIRouter(prefix="/projects")


def get_project_service() -> ProjectService:
    return ProjectService()


@router.get("/", status_code=200)
async def get_projects(service: ProjectService = Depends(get_project_service)):
    return await service.get_projects()


@router.get("/{id}", status_code=200)
async def get_project_by_id(
    id: int, service: ProjectService = Depends(get_project_service)
):
    return await service.get_project_by_id(id)


@router.post("/", status_code=201)
async def insert_project(
    project: ProjectCreate, service: ProjectService = Depends(get_project_service)
):
    return await service.insert_project(project)


@router.delete("/{id}", status_code=200)
async def delete_project(
    id: int, service: ProjectService = Depends(get_project_service)
):
    return await service.delete_project(id)
