from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, List, Optional
from app.utils.validators import PyObjectId


class ProjectCreate(BaseModel):
    github_id: int
    name: str
    description: Optional[str] = None
    html_url: str
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    languages_url: str
    image_url: Optional[str] = None


class ProjectGet(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    github_id: int
    name: str
    description: Optional[str] = None
    html_url: str
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    languages: List[str]
    languages_url: str
    image_url: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
