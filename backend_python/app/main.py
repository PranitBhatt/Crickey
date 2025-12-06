"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database import init_db, close_db
from app.middleware.error_handler import (
    error_handler,
    validation_exception_handler,
    http_exception_handler
)

# Import routers
from app.routers import auth, tournaments, teams, matches, schedule, points_table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Cricket Tournament Management API",
    description="Python/FastAPI backend with PostgreSQL",
    version="1.0.0",
    docs_url="/swagger" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    try:
        await init_db()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    await close_db()

# CORS middleware - allow localhost and Vercel deployments
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(Exception, error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# Include routers
app.include_router(auth.router)
app.include_router(tournaments.router)
app.include_router(teams.router)
app.include_router(matches.router)
app.include_router(schedule.router)
app.include_router(points_table.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cricket Tournament Management API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
