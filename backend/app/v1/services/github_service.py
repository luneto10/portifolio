import httpx
from app.v1.core.config_v1 import settings
from app.v1.models.github import GitHubRepo


async def fetch_github_repos() -> list[GitHubRepo]:
    """
    Fetches GitHub repositories using async HTTPX.
    """
    headers = (
        {"Authorization": f"Bearer {settings.GITHUB_TOKEN}"}
        if settings.GITHUB_TOKEN
        else {}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers=headers,
            params={"sort": "updated", "per_page": 100},
        )
        response.raise_for_status()

        repos = response.json()
        return [GitHubRepo(**repo) for repo in repos]
