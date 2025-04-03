import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.v1.db.prisma import connect, disconnect


@pytest.fixture(scope="session")
async def db_connection():
    # Connect to the database
    await connect()
    yield
    # Disconnect from the database
    await disconnect()


@pytest.fixture
def client(db_connection):
    # Use the TestClient with the database connection
    with TestClient(app) as client:
        yield client
