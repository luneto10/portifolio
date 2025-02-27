import logging
from typing import List, Any, Optional
from fastapi import Depends, HTTPException, Request
from httpx import HTTPStatusError
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from app.v2.models.project import (
    ProjectCreate,
    ProjectGet,
)

from app.v2.services.language import fetch_languages

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

    async def get_project_by_id(self, id: int) -> ProjectGet:
        """
        Retrieve a single project by its ID.

        :param id: The unique identifier of the project.
        :return: The project object corresponding to the provided ID.
        :raises HTTPException: If the project is not found or the database call fails.
        """
        try:
            project = await self.collection.find_one({"_id": id})

            if not project:
                raise HTTPException(
                    status_code=404, detail=f"Project with id {id} not found"
                )
            return ProjectGet(**project)
        except Exception as e:
            logger.error(f"Error getting project by id: {e}")
            raise HTTPException(status_code=500, detail="Failed to get project by id")

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
            data.pop("languages_url")

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
            raise HTTPException(
                status_code=500, detail=f"{e}: Failed to insert"
            )

    @staticmethod
    async def delete_project(id: int) -> Any:
        """
        Delete a project by its ID.

        :param id: The unique identifier of the project to delete.
        :return: The deleted project object.
        :raises HTTPException: If the project is not found or deletion fails.
        """
        raise NotImplementedError("Not implemented")
