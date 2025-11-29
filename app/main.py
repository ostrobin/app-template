"""MyApp - FastAPI application."""
import logging

from fastapi import FastAPI

from .config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="MyApp", version="0.1.0")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    """Initialize database connection on startup."""
    logger.info("Starting MyApp")


@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown."""
    logger.info("Shutting down MyApp")
