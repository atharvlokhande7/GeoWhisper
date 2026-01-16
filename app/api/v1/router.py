from fastapi import APIRouter
from app.api.v1.endpoints import location, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(location.router, prefix="/location", tags=["location"])
