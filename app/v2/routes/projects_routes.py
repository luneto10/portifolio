from fastapi import APIRouter, HTTPException, Depends, Request
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from app.v2.services.project_service import ProjectService
from app.v2.models.project import ProjectCreate, ProjectGet

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(request: Request) -> AsyncIOMotorCollection:
    collection = request.app.mongodb["projects"]
    return ProjectService(collection)


@router.get("/", status_code=200, response_model=list[ProjectGet])
async def get_projects(
    service : ProjectService = Depends(get_project_service)
):
    return await service.get_projects()


@router.get("/{id}", status_code=200, response_model=ProjectGet)
async def get_project_by_id(
    id: int, service: ProjectService = Depends(get_project_service)
):
    return await service.get_project_by_id(id)


@router.post("/", status_code=201, response_model=ProjectGet)
async def insert_project(
    project: ProjectCreate, service: ProjectService = Depends(get_project_service)
):
    return await service.insert_project(project)


@router.delete("/{id}", status_code=200, response_model=ProjectGet)
async def delete_project(
    id: int, service: ProjectService = Depends(get_project_service)
):
    return await service.delete_project(id)
