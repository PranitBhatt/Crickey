"""
FastAPI application entry point.
Mirrors Program.cs from .NET backend.
"""
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
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

# CORS middleware - allow localhost and Vercel deployments
# Using regex pattern to match localhost:5173 and all *.vercel.app domains
# Replace <MY_VERCEL_DOMAIN> with your actual Vercel domain
CORS_ORIGIN_REGEX = r"https://.*\.vercel\.app|http://localhost:5173"
# To add a specific domain, use: r"https://.*\.vercel\.app|https://<MY_VERCEL_DOMAIN>|http://localhost:5173"

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=CORS_ORIGIN_REGEX,
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
    """Health check endpoint for Render"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    import os
    # Use PORT environment variable (for Render) or default to 5000
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.DEBUG
    )

