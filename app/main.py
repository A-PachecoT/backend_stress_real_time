from contextlib import asynccontextmanager
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import (
    auth,
    questionnaire,
    questions,
    results,
    sensors,
    stress_analysis,
    users,
)
from app.core.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title="StressMinder API",
    description="API for stress monitoring and analysis",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(sensors.router)
app.include_router(questions.router)
app.include_router(results.router)
app.include_router(users.router)
app.include_router(questionnaire.router)
app.include_router(stress_analysis.router)


@app.get("/")
async def root():
    return {"message": "Welcome to StressMinder API"}
