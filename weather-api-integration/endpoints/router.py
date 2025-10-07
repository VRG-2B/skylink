"""User profile endpoints."""

import logging

from fastapi import APIRouter, HTTPException

from models import WeatherRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/location", tags=["location"])

@router.post("")
async def get_location(request: WeatherRequest):
    """Get weather information for a specific location."""

    pass
