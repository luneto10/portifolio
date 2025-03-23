from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.v2.core.config import settings
from contextlib import asynccontextmanager
import logging
import certifi

from app.v2 import models

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(
        settings.MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
    )
    await init_beanie(
        database=client[settings.MONGO_DATABASE],
        document_models=models.__all__,
    )
    yield
    client.close()
