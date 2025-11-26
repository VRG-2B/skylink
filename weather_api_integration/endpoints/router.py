"""Health check endpoint."""

from fastapi import APIRouter

from weather_api_integration.models.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Status of the API
    """
    return HealthResponse(status="ok")
