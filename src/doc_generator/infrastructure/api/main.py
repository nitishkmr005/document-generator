"""FastAPI application for document generation."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health_router

app = FastAPI(
    title="Document Generator API",
    description="Generate PDF and PPTX documents from multiple sources",
    version="0.1.0",
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api")
