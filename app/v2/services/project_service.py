import logging
from typing import List, Any, Optional
from fastapi import HTTPException
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

    @staticmethod
    async def get_projects() -> List[ProjectGet]:
        """
        Retrieve all projects.

        :return: A list of project objects.
        :raises HTTPException: If fetching projects fails.
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    async def insert_project(project: ProjectCreate) -> Any:
        """
        Insert or update a project using the upsert operation.
        The upsert will update an existing project if it exists; otherwise, it will create a new one.
        In the create branch, it uses nested writes to create or connect languages.

        :param project: A ProjectCreate instance with project data.
        :return: The inserted or updated project object.
        :raises HTTPException: If inserting/updating the project fails.
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    async def get_project_by_id(id: int) -> ProjectGet:
        """
        Retrieve a single project by its ID.

        :param id: The unique identifier of the project.
        :return: The project object corresponding to the provided ID.
        :raises HTTPException: If the project is not found or the database call fails.
        """
        raise NotImplementedError("Not implemented")

    @staticmethod
    async def delete_project(id: int) -> Any:
        """
        Delete a project by its ID.

        :param id: The unique identifier of the project to delete.
        :return: The deleted project object.
        :raises HTTPException: If the project is not found or deletion fails.
        """
        raise NotImplementedError("Not implemented")
