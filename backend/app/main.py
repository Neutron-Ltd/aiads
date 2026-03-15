from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from app.api.v1.routes import projects
from app.config import settings
from app.database import engine


def _run_migrations():
    """Add new columns to existing tables (SQLite)."""
    from sqlalchemy import text

    with engine.connect() as conn:
        try:
            conn.execute(
                text(
                    'ALTER TABLE project ADD COLUMN google_ads_customer_id TEXT DEFAULT ""'
                )
            )
            conn.commit()
        except Exception:
            pass  # Column likely already exists


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    if "sqlite" in settings.database_url:
        _run_migrations()
    yield


app = FastAPI(
    title="Ads Co-Pilot API",
    description="Backend API for Ads Co-Pilot - Human-in-the-loop AI for Google Ads",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/v1", tags=["projects"])


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.environment,
        "google_ads_configured": settings.google_ads_configured,
    }
