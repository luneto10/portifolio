from typing import List, Any
from fastapi import Depends, HTTPException, status
from httpx import HTTPStatusError

from app.v2.models.project import Project, ProjectCreate, ProjectGet, ProjectUpdate
from app.v2.services.language import fetch_languages
from app.utils.validators import PyObjectId
from app.utils.logger import logger
from app.utils.error_handler import handle_error

project_collection = Project

class ProjectService:
    """
    Service class for managing project operations using Beanie.
    """

    @handle_error
    async def get_projects(self) -> List[ProjectGet]:
        projects = await project_collection.find_all().to_list()
        return [ProjectGet(**project.model_dump(by_alias=True)) for project in projects]

    @handle_error
    async def get_project_by_id(self, id: PyObjectId, user_id: str) -> ProjectGet:
        project = await project_collection.get(id)
        print(user_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {id} not found",
            )
        return ProjectGet(**project.model_dump(by_alias=True))

    @handle_error
    async def get_project_by_github_id(self, github_id: int) -> ProjectGet:
        project = await project_collection.find_one(project_collection.github_id == github_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with github_id {github_id} not found",
            )
        return ProjectGet(**project.model_dump(by_alias=True))

    @handle_error
    async def insert_project(self, project_create: ProjectCreate) -> ProjectGet:
        project_exists = await project_collection.find_one(project_collection.github_id == project_create.github_id)
        if project_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Project with github_id {project_create.github_id} already exists",
            )

        project_data = project_create.model_dump()
        languages = await fetch_languages(project_create.languages_url)
        project_data["languages"] = languages

        new_project = Project(**project_data)
        await new_project.insert()
        return ProjectGet(**new_project.model_dump(by_alias=True))

    @handle_error
    async def update_project(self, id: PyObjectId, project_update: ProjectUpdate) -> ProjectGet:
        project = await project_collection.get(id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        languages = await fetch_languages(project.languages_url)
        update_data = project_update.model_dump(exclude_unset=True)
        update_data["languages"] = languages

        for key, value in update_data.items():
            setattr(project, key, value)

        await project.save()
        return ProjectGet(**project.model_dump(by_alias=True))

    @handle_error
    async def delete_projects(self) -> Any:
        delete_result = await project_collection.find_all().delete()
        return {
            "message": "All projects deleted successfully",
            "deleted_count": getattr(delete_result, "deleted_count", 0),
        }

    @handle_error
    async def delete_project(self, id: PyObjectId) -> Any:
        project = await project_collection.get(id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {id} not found",
            )
        await project.delete()
        return {
            "message": f"Project with id {id} deleted successfully",
            "deleted_id": str(id),
        }
