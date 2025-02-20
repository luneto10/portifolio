import json
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from models.schemas.project import ProjectCreate
import pytest


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_create_project(client):
    test_project = {
        "id": 12345,
        "name": "Test Project",
        "description": "Test description",
        "html_url": "https://github.com/test/test-project",
        "pushed_at": "2024-01-15T12:00:00Z",
        "created_at": "2024-01-10T09:30:00Z",
        "updated_at": "2024-01-10T09:30:00Z",
        "languages_url": "https://api.github.com/repos/test/test-project/languages",
    }

    response = client.post("/projects/", json=test_project)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
    assert response.json()["id"] == 12345


def test_create_project_with_invalid_data(client):
    response = client.post("/projects/", json={"invalid_field": "invalid_value"})
    assert response.status_code == 422


def test_get_projects(client):
    response = client.get("/projects/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_project_by_id(client):
    response = client.get("/projects/12345")
    assert response.status_code == 200
    assert response.json()["id"] == 12345
    assert response.json()["name"] == "Test Project"


def test_get_project_by_id_not_found(client):
    response = client.get("/projects/123456")
    assert response.status_code == 404


@pytest.mark.dependency(depends=["test_create_project"])
@pytest.mark.last
def test_delete_project(client):
    response = client.delete("/projects/12345")
    assert response.status_code == 200
    assert response.json()["id"] == 12345
