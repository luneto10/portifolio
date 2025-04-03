from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.v2.routes import (
    github_routes as github_routes_v2,
    projects_routes as projects_routes_v2,
)
from app.v2.db import mongoDB

from app.v2.auth.jwt_bearer import JWTBearer
from app.v2.routes import admin_routes

app = FastAPI(lifespan=mongoDB.lifespan)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


# Include routers
# app.include_router(projects_routes.router, prefix="/v1")
@app.get("/")
def root():
    return "Server is running"


app.include_router(github_routes_v2.router)

# Include routers v2
app.include_router(projects_routes_v2.router, prefix="/v2", dependencies=[Depends(JWTBearer())])
app.include_router(admin_routes.router, prefix="/v2")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
