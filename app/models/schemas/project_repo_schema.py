from pydantic import BaseModel
from typing import Optional


class ProjectCreate(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    html_url: str
    pushed_at: str
    created_at: str
    updated_at: str
    languages_url: str


class ProjectGet(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    html_url: str
    pushed_at: str
    created_at: str
    updated_at: str
    languages_url: str
