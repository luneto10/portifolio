from contextlib import asynccontextmanager
from fastapi import FastAPI
from prisma import Prisma

prisma = Prisma()


async def connect():
    await prisma.connect()


async def disconnect():
    await prisma.disconnect()


def get_prisma():
    return prisma


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await disconnect()
