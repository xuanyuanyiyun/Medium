from fastapi import APIRouter
from app.api import projects, contents

api_router = APIRouter()

api_router.include_router(projects.router)
api_router.include_router(contents.router)
