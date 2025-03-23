from datetime import datetime
from pydantic import BaseModel
from typing import Any, List, Optional


class ProjectCreate(BaseModel):
    id: int
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

    class Config:
        from_attributes = True


class ProjectGet(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    html_url: str
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    languages: List[LanguageResponse]

    class Config:
        from_attributes = True

    @classmethod
    def from_prisma(cls, data: dict) -> "ProjectGet":
        """
        Converts a Prisma project record into a ProjectGet instance.
        Assumes that data["languages"] is a list of objects where each object has a key "language"
        that contains the actual language data.
        """
        data = data.copy()
        # Extract the nested language data from the join table.
        # Each item in data["languages"] is assumed to be a dict with key "language"
        data["languages"] = [lang["language"] for lang in data.get("languages", [])]
        return cls.model_validate(data)
