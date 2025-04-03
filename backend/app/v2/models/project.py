from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List, Optional
from app.utils.validators import PyObjectId
from beanie import Document, Save, before_event


class Project(Document):
    github_id: int = Field(..., example=123456)
    name: str = Field(..., example="My Awesome Project")
    description: Optional[str] = Field(None, example="A description of my project")
    html_url: str = Field(..., example="https://github.com/user/my-awesome-project")
    pushed_at: datetime = Field(..., example="2023-03-01T12:00:00+00:00")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    languages: List[str] = Field(..., example=["Python", "JavaScript"])
    languages_url: str = Field(..., example="https://api.github.com/repos/user/my-awesome-project/languages")
    image_url: Optional[str] = Field(None, example="https://example.com/my-awesome-project.png")

    class Settings:
        name = "projects"
        indexes = ["github_id"]
        
    @before_event(Save)
    def pre_save(self):
        self.updated_at = datetime.now(timezone.utc)
        

    class Config:
        json_schema_extra = {
            "example": {
                "github_id": 123456,
                "name": "My Awesome Project",
                "description": "A description of my project",
                "html_url": "https://github.com/user/my-awesome-project",
                "pushed_at": "2023-03-01T12:00:00+00:00",
                "created_at": "2023-02-28T12:00:00+00:00",
                "updated_at": "2023-03-01T12:00:00+00:00",
                "languages": ["Python", "JavaScript"],
                "languages_url": "https://api.github.com/repos/user/my-awesome-project/languages",
                "image_url": "https://example.com/my-awesome-project.png"
            }
        }


class ProjectCreate(BaseModel):
    # Notice the absence of id, created_at, and updated_at.
    github_id: int = Field(..., example=123456)
    name: str = Field(..., example="My Awesome Project")
    description: Optional[str] = Field(None, example="A description of my project")
    html_url: str = Field(..., example="https://api.github.com/repos/Datquangbui1011/Cornhack-Project")
    pushed_at: datetime = Field(..., example="2023-03-01T12:00:00+00:00")
    languages_url: str = Field(..., example="https://api.github.com/repos/Datquangbui1011/Cornhack-Project/languages")
    image_url: Optional[str] = Field(None, example="https://example.com/my-awesome-project.png")

    class Config:
        json_schema_extra = {
            "example": {
                "github_id": 123456,
                "name": "My Awesome Project",
                "description": "A description of my project",
                "html_url": "https://api.github.com/repos/Datquangbui1011/Cornhack-Project",
                "pushed_at": "2023-03-01T12:00:00+00:00",
                "languages_url": "https://api.github.com/repos/Datquangbui1011/Cornhack-Project/languages",
                "image_url": "https://example.com/my-awesome-project.png"
            }
        }


class ProjectGet(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, example="64a50b684f6b1e2b68a3d1f4")
    github_id: int = Field(..., example=123456)
    name: str = Field(..., example="My Awesome Project")
    description: Optional[str] = Field(None, example="A description of my project")
    html_url: str = Field(..., example="https://github.com/user/my-awesome-project")
    pushed_at: datetime = Field(..., example="2023-03-01T12:00:00+00:00")
    created_at: datetime = Field(..., example="2023-02-28T12:00:00+00:00")
    updated_at: datetime = Field(..., example="2023-03-01T12:00:00+00:00")
    languages: List[str] = Field(..., example=["Python", "JavaScript"])
    languages_url: str = Field(..., example="https://api.github.com/repos/user/my-awesome-project/languages")
    image_url: Optional[str] = Field(None, example="https://example.com/my-awesome-project.png")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "_id": "64a50b684f6b1e2b68a3d1f4",
                "github_id": 123456,
                "name": "My Awesome Project",
                "description": "A description of my project",
                "html_url": "https://github.com/user/my-awesome-project",
                "pushed_at": "2023-03-01T12:00:00+00:00",
                "created_at": "2023-02-28T12:00:00+00:00",
                "updated_at": "2023-03-01T12:00:00+00:00",
                "languages": ["Python", "JavaScript"],
                "languages_url": "https://api.github.com/repos/user/my-awesome-project/languages",
                "image_url": "https://example.com/my-awesome-project.png"
            }
        }


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, example="My Awesome Project Updated")
    description: Optional[str] = Field(None, example="An updated description for my project")
    image_url: Optional[str] = Field(None, example="https://example.com/my-awesome-project-updated.png")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Awesome Project Updated",
                "description": "An updated description for my project",
                "image_url": "https://example.com/my-awesome-project-updated.png"
            }
        }
