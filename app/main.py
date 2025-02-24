from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.v1.routes import github_routes, projects_routes
from app.v1.db.prisma import connect, disconnect


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await disconnect()


app = FastAPI(lifespan=lifespan)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

# Include routers
app.include_router(projects_routes.router, prefix="/v1")
app.include_router(github_routes.router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
