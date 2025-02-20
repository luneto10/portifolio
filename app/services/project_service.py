import logging
from typing import List, Any, Optional
from fastapi import HTTPException
from prisma.errors import RecordNotFoundError, PrismaError
from app.models.schemas.project_repo_schema import ProjectCreate
from app.utils.prisma import get_prisma

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

    def __init__(self, prisma_client: Optional[Any] = None):
        """
        Initialize the ProjectService with a Prisma client.

        :param prisma_client: An instance of the Prisma client. If not provided,
                              get_prisma() will be used to obtain one.
        """
        self.prisma = prisma_client or get_prisma()

    async def get_projects(self) -> List[Any]:
        """
        Retrieve all projects.

        :return: A list of project objects.
        :raises HTTPException: If fetching projects fails.
        """
        try:
            projects = await self.prisma.project.find_many()
            return projects
        except PrismaError as e:
            logger.error(f"Prisma error fetching projects: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch projects")

    async def insert_project(self, project: ProjectCreate) -> Any:
        """
        Insert or update a project using the upsert operation.
        The upsert will update an existing project if it exists; otherwise, it will create a new one.

        :param project: A ProjectCreate instance with project data.
        :return: The inserted or updated project object.
        :raises HTTPException: If inserting/updating the project fails.
        """
        try:
            new_project = await self.prisma.project.upsert(
                where={"id": project.id},
                data={
                    "update": project.model_dump(),
                    "create": project.model_dump(),  # Adjust if create data differs from update data
                },
            )
            return new_project
        except PrismaError as e:
            logger.error(f"Prisma error inserting project: {e}")
            raise HTTPException(
                status_code=400, detail=f"{e}: Failed to insert project"
            )

    async def get_project_by_id(self, id: int) -> Any:
        """
        Retrieve a single project by its ID.

        :param id: The unique identifier of the project.
        :return: The project object corresponding to the provided ID.
        :raises HTTPException: If the project is not found or the database call fails.
        """
        try:
            project = await self.prisma.project.find_unique(where={"id": id})
            if not project:
                raise HTTPException(
                    status_code=404, detail=f"Project with id {id} not found"
                )
            return project
        except PrismaError as e:
            logger.error(f"Prisma error getting project by id: {e}")
            raise HTTPException(status_code=500, detail="Failed to get project by id")

    async def delete_project(self, id: int) -> Any:
        """
        Delete a project by its ID.

        :param id: The unique identifier of the project to delete.
        :return: The deleted project object.
        :raises HTTPException: If the project is not found or deletion fails.
        """
        try:
            deleted_project = await self.prisma.project.delete(where={"id": id})
            if not deleted_project:
                logger.error(f"Project with id {id} not found for deletion")
                raise HTTPException(
                    status_code=404, detail=f"Project with id {id} not found"
                )
            return deleted_project
        except PrismaError as e:
            logger.error(f"Prisma error deleting project: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete project")
