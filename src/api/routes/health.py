"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "multi-agent-api",
    }


@router.get("/ready")
async def readiness_check() -> dict:
    """Readiness check endpoint."""
    # Add actual dependency checks here (Redis, DB, etc.)
    return {
        "status": "ready",
        "checks": {
            "api": True,
        },
    }
