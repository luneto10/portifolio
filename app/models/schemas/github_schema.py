from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GitHubRepo(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    html_url: str
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    languages_url: str  