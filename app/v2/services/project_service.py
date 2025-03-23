from typing import List, Any
from fastapi import HTTPException
from httpx import HTTPStatusError

from app.v2.models.project import Project, ProjectCreate, ProjectGet, ProjectUpdate
from app.v2.services.language import fetch_languages
from app.utils.validators import PyObjectId

from app.utils.logger import logger

project_colletion = Project
class ProjectService:
    """
    Service class for managing project operations using Beanie.
    """

    async def get_projects(self) -> List[ProjectGet]:
        try:
            projects = await project_colletion.find_all().to_list()
            return [ProjectGet(**project.model_dump(by_alias=True)) for project in projects]
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch projects")

    async def get_project_by_id(self, id: PyObjectId) -> ProjectGet:
        try:
            project = await project_colletion.get(id)
            if not project:
                raise HTTPException(status_code=404, detail=f"Project with id {id} not found")
            return ProjectGet(**project.model_dump(by_alias=True))
        except Exception as e:
            logger.error(f"Error getting project by id: {e}")
            raise HTTPException(status_code=500, detail="Failed to get project by id")

    async def get_project_by_github_id(self, github_id: int) -> ProjectGet:
        try:
            project = await project_colletion.find_one(project_colletion.github_id == github_id)
            if not project:
                raise HTTPException(status_code=404, detail=f"Project with github_id {github_id} not found")
            return ProjectGet(**project.model_dump(by_alias=True))
        except Exception as e:
            logger.error(f"Error getting project by github_id: {e}")
            raise HTTPException(status_code=500, detail="Failed to get project by github_id")

    async def insert_project(self, project_create: ProjectCreate) -> ProjectGet:
        try:
            project_exists = await project_colletion.find_one(project_colletion.github_id == project_create.github_id)
            if project_exists:
                raise HTTPException(
                    status_code=409,
                    detail=f"Project with github_id {project_create.github_id} already exists",
                )

            project_data = project_create.model_dump()
            languages = await fetch_languages(project_create.languages_url)
            project_data["languages"] = languages

            new_project = Project(**project_data)
            await new_project.insert()
            return ProjectGet(**new_project.model_dump(by_alias=True))
        except HTTPStatusError as http:
            logger.error(f"Error fetching languages: {http}")
            raise HTTPException(
                status_code=http.response.status_code,
                detail=f"{http}: Failed to fetch languages",
            )
        except Exception as e:
            logger.error(f"Error inserting project: {e}")
            raise HTTPException(status_code=500, detail=f"{e}: Failed to insert project")

    async def update_project(self, id: PyObjectId, project_update: ProjectUpdate) -> ProjectGet:
        try:
            project = await project_colletion.get(id)
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")

            # Optionally, re-fetch languages if needed
            languages = await fetch_languages(project.languages_url)
            update_data = project_update.model_dump(exclude_unset=True)
            update_data["languages"] = languages

            for key, value in update_data.items():
                setattr(project, key, value)

            await project.save()
            return ProjectGet(**project.model_dump(by_alias=True))
        except HTTPStatusError as http:
            logger.error(f"Error updating project: {http}")
            raise HTTPException(
                status_code=http.response.status_code,
                detail=f"{http}: Failed to update project",
            )
        except Exception as e:
            logger.error(f"Error updating project: {e}")
            raise HTTPException(status_code=500, detail=f"{e}: Failed to update project")

    async def delete_projects(self) -> Any:
        try:
            delete_result = await project_colletion.find_all().delete()
            return {
                "message": "All projects deleted successfully",
                "deleted_count": getattr(delete_result, "deleted_count", None),
            }
        except Exception as e:
            logger.error(f"Error deleting projects: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete projects")

    async def delete_project(self, id: PyObjectId) -> Any:
        try:
            project = await project_colletion.get(id)
            if not project:
                raise HTTPException(status_code=404, detail=f"Project with id {id} not found")
            await project.delete()
            return {
                "message": f"Project with id {id} deleted successfully",
                "deleted_id": str(id)
            }
        except Exception as e:
            logger.error(f"Error deleting project: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete project")
