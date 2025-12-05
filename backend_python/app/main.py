"""
FastAPI application entry point.
Mirrors Program.cs from .NET backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

from app.config import settings
from app.database import initialize_firebase
from app.middleware.error_handler import (
    error_handler,
    validation_exception_handler,
    http_exception_handler
)

# Import routers
from app.routers import tournaments, teams, matches, auth, points_table, notifications

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Cricket Tournament Management API",
    description="Python/FastAPI backend migrated from .NET 8",
    version="1.0.0",
    docs_url="/swagger" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Initialize Firebase on startup
@app.on_event("startup")
async def startup_event():
    """Initialize Firebase Admin SDK on application startup"""
    try:
        initialize_firebase()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

# CORS middleware - mirrors .NET "AllowAll" policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers - mirrors ErrorHandlingMiddleware.cs
app.add_exception_handler(Exception, error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# Include routers - mirrors MapControllers() in .NET
app.include_router(tournaments.router)
app.include_router(teams.router)
app.include_router(matches.router)
app.include_router(auth.router)
app.include_router(points_table.router)
app.include_router(notifications.router)


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
        host="0.0.0.0",
        port=5000,
        reload=settings.DEBUG
    )

