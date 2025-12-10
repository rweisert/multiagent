"""FastAPI application factory."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import agents, workflows, health
from src.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    # Startup
    settings = get_settings()
    print(f"Starting Multi-Agent API on {settings.api_host}:{settings.api_port}")

    yield

    # Shutdown
    print("Shutting down Multi-Agent API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Multi-Agent LLM API",
        description="API for orchestrating multi-agent LLM workflows",
        version="0.1.0",
        lifespan=lifespan,
        debug=settings.api_debug,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
    app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["Workflows"])

    return app


# Create app instance for uvicorn
app = create_app()
