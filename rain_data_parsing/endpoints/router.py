"""Precipitation endpoint."""

import logging

from fastapi import APIRouter, HTTPException, Query

from rain_data_parsing.models.precipitation import PrecipitationResponse
from rain_data_parsing.services.precipitation import get_precipitation

logger = logging.getLogger(__name__)
router = APIRouter(tags=["precipitation"])


@router.get("/precipitation", response_model=PrecipitationResponse)
async def get_precipitation_endpoint(city: str = Query(..., description="City name")):
    """
    Get precipitation data (rain and thunder status) for a city.
    
    Args:
        city (str): City name
        
    Returns:
        PrecipitationResponse: Rain and thunder as booleans
        
    Raises:
        HTTPException: If city not found or API error occurs
    """
    try:
        logger.info(f"Fetching precipitation data for: {city}")
        data = get_precipitation(city)
        return PrecipitationResponse(**data)
    except ValueError as e:
        logger.error(f"City not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching precipitation data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching precipitation data: {str(e)}")
