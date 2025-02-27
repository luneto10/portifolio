from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, List, Optional

from app.utils.validators import PyObjectId


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    html_url: str
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    languages_url: str


class LanguageResponse(BaseModel):
    id: int
    language: str


class ProjectGet(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = None
    html_url: str
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    languages: List[LanguageResponse]
