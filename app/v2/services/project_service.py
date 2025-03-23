import logging
from typing import List, Any
from fastapi import Depends, HTTPException
from httpx import HTTPStatusError
from motor.motor_asyncio import (
    AsyncIOMotorCollection,
)
from bson import ObjectId
from pymongo import ReturnDocument
from app.v2.models.project import (
    ProjectCreate,
    ProjectGet,
    ProjectUpdate,
)

from app.v2.services.language import fetch_languages
from app.utils.validators import PyObjectId

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class ProjectService:
    """
    Service class for managing project operations.
    """

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_projects(self) -> List[ProjectGet]:
        """
        Retrieve all projects.
        :return: A list of project objects.
        :raises HTTPException: If fetching projects fails.
        """
        try:
            projects = await self.collection.find().to_list(length=None)
            return [ProjectGet(**project) for project in projects]
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch projects")

    async def get_project_by_id(self, id: PyObjectId) -> ProjectGet:
        """
        Retrieve a single project by its ID.

        :param id: The unique identifier of the project.
        :return: The project object corresponding to the provided ID.
        :raises HTTPException: If the project is not found or the database call fails.
        """
        try:
            project = await self.collection.find_one({"_id": ObjectId(id)})

            if not project:
                raise HTTPException(
                    status_code=404, detail=f"Project with id {id} not found"
                )
            return ProjectGet(**project)
        except Exception as e:
            logger.error(f"Error getting project by id: {e}")
            raise HTTPException(status_code=500, detail="Failed to get project by id")
        
    async def get_project_by_github_id(self, github_id: str) -> ProjectGet:
        try:
            project = await self.collection.find_one({"github_id": github_id})

            if not project:
                raise HTTPException(
                    status_code=404, detail=f"Project with github_id {github_id} not found"
                )
            return ProjectGet(**project)
        except Exception as e:
            logger.error(f"Error getting project by github_id: {e}")
            raise HTTPException(status_code=500, detail="Failed to get project by github_id")

    async def insert_project(self, project: ProjectCreate) -> ProjectGet:
        """
        Insert or update a project using the upsert operation.

        :param project: A ProjectCreate instance with project data.
        :return: The inserted project object.
        :raises HTTPException: If inserting/updating the project fails.
        """
        try:
            project_exists = await self.collection.find_one(
                {"github_id": project.github_id}
            )
            if project_exists:
                raise HTTPException(
                    status_code=409,
                    detail=f"Project with github_id {project.github_id} already exists",
                )

            languages = await fetch_languages(project.languages_url)

            data = project.model_dump(mode="python")

            data["languages"] = languages

            result = await self.collection.insert_one(data)

            inserted = await self.collection.find_one({"_id": result.inserted_id})
            return ProjectGet(**inserted)

        except HTTPStatusError as http:
            logger.error(f"Error fetching languages: {http}")
            raise HTTPException(
                status_code=http.response.status_code,
                detail=f"{http}: Failed to fetch languages",
            )
        except Exception as e:
            logger.error(f"Error inserting: {e}")
            raise HTTPException(status_code=500, detail=f"{e}: Failed to insert")

    async def update_project(
        self, id: PyObjectId, project: ProjectUpdate
    ) -> ProjectGet:
        try:
            existing_project = await self.collection.find_one({"_id": ObjectId(id)})
            if not existing_project:
                raise HTTPException(status_code=404, detail="Project not found")
            existing_project = ProjectGet(**existing_project)
            languages = await fetch_languages(existing_project.languages_url)

            update_data = project.model_dump(exclude_unset=True, mode="python")
            update_data["languages"] = languages

            result = await self.collection.update_one(
                {"_id": ObjectId(id)}, {"$set": update_data}
            )
            return {
                "message": f"Project with id {id} updated successfully",
                "modified_count": result.modified_count,
            }
        except HTTPStatusError as http:
            logger.error(f"Error fetching updating project: {http}")
            raise HTTPException(
                status_code=http.response.status_code,
                detail=f"{http}: Failed to update project",
            )
        except Exception as e:
            logger.error(f"Error updating project: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"{e}: Failed to update project",
            )

    async def delete_projects(self) -> Any:
        try:
            result = await self.collection.delete_many({})
            return {
                "message": "All projects deleted successfully",
                "deleted_count": result.deleted_count,
            }
        except Exception as e:
            logger.error(f"Error deleting projects: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete projects")
        
    async def delete_project(self, id: PyObjectId) -> Any:
        """
        Delete a project by its ID.

        :param id: The unique identifier of the project to delete.
        :return: The deleted project object.
        :raises HTTPException: If the project is not found or deletion fails.
        """
        try:
            delete_project = await self.collection.delete_one({"_id": ObjectId(id)})
            if delete_project.deleted_count == 0:
                raise HTTPException(
                    status_code=404, detail=f"Project with id {id} not found"
                )
            return {
                "message": f"Project with id {id} deleted successfully",
                "deleted_count": delete_project.deleted_count,
            }
        except Exception as e:
            logger.error(f"Error deleting project: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete project")
