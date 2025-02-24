import httpx
from app.v1.core.config import settings

async def fetch_languages(language_url: str) -> list[str]:
    """
    Fetches GitHub repositories using async HTTPX.
    """
    headers = {"Authorization": f"Bearer {settings.GITHUB_TOKEN}"} if settings.GITHUB_TOKEN else {}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            language_url,
            headers=headers,
        )
        response.raise_for_status()
        
        languages = list(dict(response.json()).keys())
        return languages