from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from app.utils.validators import PyObjectId
from beanie import Document, Save, before_event


class Project(Document):
    github_id: int 
    name: str 
    description: Optional[str] 
    html_url: str 
    pushed_at: datetime 
    created_at: datetime 
    updated_at: datetime 
    languages: List[str] 
    languages_url: str 
    image_url: Optional[str] 

    class Settings:
        name = "projects"
        indexes = ["github_id"]
        
    @before_event(Save)
    def pre_save(self):
        self.updated_at = datetime.now(timezone.utc)
        
    model_config = ConfigDict(
        json_schema_extra={
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
    )


class ProjectCreate(BaseModel):
    # Notice the absence of id, created_at, and updated_at.
    github_id: int 
    name: str 
    description: Optional[str] 
    html_url: str 
    pushed_at: datetime 
    languages_url: str 
    image_url: Optional[str] 

    model_config = ConfigDict(
        json_schema_extra={
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
    )


class ProjectGet(BaseModel):
    id: Optional[PyObjectId] 
    github_id: int 
    name: str 
    description: Optional[str] 
    html_url: str 
    pushed_at: datetime 
    created_at: datetime 
    updated_at: datetime 
    languages: List[str] 
    languages_url: str 
    image_url: Optional[str] 

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
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
    )


class ProjectUpdate(BaseModel):
    name: Optional[str] 
    description: Optional[str] 
    image_url: Optional[str] 

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "My Awesome Project Updated",
                "description": "An updated description for my project",
                "image_url": "https://example.com/my-awesome-project-updated.png"
            }
        }
    )
