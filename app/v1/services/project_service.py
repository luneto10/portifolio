import logging
from typing import List, Any, Optional
from fastapi import HTTPException
from prisma.errors import RecordNotFoundError, PrismaError
from app.v1.models.project import (
    ProjectCreate,
    ProjectGet,
)
from app.v1.db.prisma import get_prisma
from app.v1.services.language import fetch_languages

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

    async def get_projects(self) -> List[ProjectGet]:
        """
        Retrieve all projects.

        :return: A list of project objects.
        :raises HTTPException: If fetching projects fails.
        """
        try:
            projects = await self.prisma.project.find_many(
                include={"languages": {"include": {"language": True}}}
            )
            return [
                ProjectGet.from_prisma(project.model_dump(mode="python"))
                for project in projects
            ]
        except PrismaError as e:
            logger.error(f"Prisma error fetching projects: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch projects")

    async def insert_project(self, project: ProjectCreate) -> Any:
        """
        Insert or update a project using the upsert operation.
        The upsert will update an existing project if it exists; otherwise, it will create a new one.
        In the create branch, it uses nested writes to create or connect languages.

        :param project: A ProjectCreate instance with project data.
        :return: The inserted or updated project object.
        :raises HTTPException: If inserting/updating the project fails.
        """
        try:
            # Fetch languages from an external source (returns a list of language names, e.g. ["Python", "JavaScript"])
            languages = await fetch_languages(project.languages_url)

            data = {
                **project.model_dump(),
                "languages": {
                    "create": [
                        {
                            "language": {
                                "connectOrCreate": {
                                    "where": {"language": lang},
                                    "create": {"language": lang},
                                }
                            }
                        }
                        for lang in languages
                    ]
                },
            }
            new_project = await self.prisma.project.create(data=data)
            return await self.get_project_by_id(new_project.id)
        except PrismaError as e:
            logger.error(f"Prisma error inserting project: {e}")
            raise HTTPException(
                status_code=400, detail=f"{e}: Failed to insert project"
            )

    async def get_project_by_id(self, id: int) -> ProjectGet:
        """
        Retrieve a single project by its ID.

        :param id: The unique identifier of the project.
        :return: The project object corresponding to the provided ID.
        :raises HTTPException: If the project is not found or the database call fails.
        """
        try:
            project = await self.prisma.project.find_unique(
                where={"id": id},
                include={"languages": {"include": {"language": True}}},
            )
            if not project:
                raise HTTPException(
                    status_code=404, detail=f"Project with id {id} not found"
                )
            return ProjectGet.from_prisma(project.model_dump(mode="python"))
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
            await self.prisma.projectlanguage.delete_many(where={"projectId": id})

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
