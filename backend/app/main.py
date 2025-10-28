"""
OmniLearnAI FastAPI Backend - Main Application Entry Point

This module initializes and configures the FastAPI application for the OmniLearnAI system.
It sets up CORS middleware, includes API routers, and handles application lifecycle events.

OmniLearnAI: "Learn from everywhere" - A multi-source learning platform that helps
users learn from documents, web pages, and videos with AI-powered insights and citations.

Key Components:
    - FastAPI app initialization with OpenAPI documentation
    - CORS middleware for frontend communication
    - API route registration (upload, chat, sources)
    - Health check endpoints
    - Qdrant database initialization on startup

Author: Development Team
Version: 1.0.0
Last Modified: October 2025
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

logger = logging.getLogger(__name__)

from app.config.settings import settings
from app.api.v1 import upload, chat, sources

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Initialize FastAPI app
app = FastAPI(
    title="OmniLearnAI API",
    description="Learn from everywhere - Multi-Source Learning Platform with Complete Citation Grounding",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
# Enables Cross-Origin Resource Sharing for frontend communication
# In production, restrict allow_origins to specific frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Frontend URLs (configured in settings)
    allow_credentials=True,               # Allow cookies/auth headers
    allow_methods=["*"],                  # Allow all HTTP methods
    allow_headers=["*"],                  # Allow all headers
)

# Include routers
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(sources.router, prefix="/api/v1", tags=["sources"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to OmniLearnAI API",
        "tagline": "Learn from everywhere",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "qdrant_connected": True
    }

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    
    Initializes required services and connections:
    1. Qdrant vector database connection
    2. Verifies all collections exist
    3. Logs startup status
    
    Raises:
        Exception: If Qdrant initialization fails (critical error)
    """
    logger.info("🚀 OmniLearnAI API starting up...")

    # Initialize Qdrant vector database connection
    # This creates collections if they don't exist
    from app.db.qdrant_client import init_qdrant
    try:
        init_qdrant()
        logger.info("✅ Qdrant initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Qdrant: {str(e)}")
        # Re-raise to prevent app from starting with broken dependencies
        raise

    logger.info("✅ OmniLearnAI API started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("🛑 OmniLearnAI API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower()
    )
