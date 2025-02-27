from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.v2.core.config import settings
from contextlib import asynccontextmanager
import logging
import certifi

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    logger.info("Starting DB lifespan...")
    app.mongodb_client = AsyncIOMotorClient(
        settings.MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
    )
    app.mongodb = app.mongodb_client.get_database(settings.MONGO_DATABASE)

    try:
        ping_response = await app.mongodb.command("ping")
        if int(ping_response.get("ok", 0)) != 1:
            raise Exception("Problem connecting to database cluster.")
        else:
            logger.info("Connected to database cluster.")
    except Exception as e:
        logger.error(f"Error during DB startup: {str(e)}", exc_info=True)
        raise
    yield
    logger.info("Shutting down DB connection...")
    app.mongodb_client.close()
