from urllib.parse import quote_plus
from beanie import init_beanie
import pytest
from fastapi.testclient import TestClient
from app.main import app
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import certifi
from app.v2 import models
from app.v2.core.config import Settings

async def _test_lifespan(app):
    client = AsyncIOMotorClient(
        Settings().MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
    )
    await init_beanie(
        database=client["test"],
        document_models=models.__all__,
    )
    yield
    client.close()

@pytest.fixture
def client():
    app.router.lifespan_context = _test_lifespan
    with TestClient(app) as client:
        yield client


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server is running"

def test_get_github_repos(client):
    response = client.get(f"/github/repos")
    assert response.status_code == 200