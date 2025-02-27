from fastapi import APIRouter, HTTPException
import httpx
from app.v2.services.github_service import fetch_github_repos
from app.v2.models.github import GitHubRepo

router = APIRouter(prefix="/github", tags=["Github"])


@router.get("/repos", response_model=list[GitHubRepo])
async def get_github_repos():
    try:
        return await fetch_github_repos()
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail="GitHub API error"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
