from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import create_db_and_tables
from app.api.routes import router as pessoas_router
from app.api.webhook import router as webhook_router

# Create FastAPI app
app = FastAPI(
    title="WayV Integration API",
    description="API para integração com formulários WayV",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pessoas_router)
app.include_router(webhook_router)

# Create database and tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "WayV Integration API",
        "documentation": "/docs",
    }
