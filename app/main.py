from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.v1.routes import github_routes, projects_routes
from app.v2.routes import (
    github_routes as github_routes_v2,
    projects_routes as projects_routes_v2,
)
from app.v2.db.mongoDB import db_lifespan as db_lifespan_mongo

app = FastAPI(lifespan=db_lifespan_mongo)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)
# Include routers
# app.include_router(projects_routes.router, prefix="/v1")


app.include_router(github_routes_v2.router)

# Include routers v2
app.include_router(projects_routes_v2.router, prefix="/v2")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
