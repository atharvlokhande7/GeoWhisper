from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine
from app.models.base import Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Startup event to create tables (simplistic for dev, usually use Alembic)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to GeoWhisper API"}
