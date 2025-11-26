"""Time endpoint."""

import logging

from fastapi import APIRouter, HTTPException, Query

from sun_position_translation.models.time import TimeResponse
from sun_position_translation.services.time_service import get_current_ticks

logger = logging.getLogger(__name__)
router = APIRouter(tags=["time"])


@router.get("/time", response_model=TimeResponse)
async def get_time_endpoint(city: str = Query(..., description="City name")):
    """
    Get current Minecraft ticks for a city.
    
    Calculates the current time in Minecraft ticks by interpolating
    between sunrise (0 ticks) and sunset (12000 ticks) based on the
    current local time in the specified city.
    
    Args:
        city (str): City name
        
    Returns:
        TimeResponse: Current Minecraft ticks (0-23999)
        
    Raises:
        HTTPException: If city not found or API error occurs
    """
    try:
        logger.info(f"Fetching time ticks for: {city}")
        ticks = get_current_ticks(city)
        return TimeResponse(ticks=ticks)
    except ValueError as e:
        logger.error(f"City not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching time data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching time data: {str(e)}")
