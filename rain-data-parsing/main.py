"""
Precipitation API with FastAPI.
Provides /precipitation endpoint for fetching thunder data.
"""

from fastapi import FastAPI, HTTPException, Query
from models.weather import ThunderResponse
from services.weather_service import get_thunder
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Precipitation API", version="1.0.0")


@app.get("/precipitation", response_model=ThunderResponse)
async def get_precipitation_endpoint(city: str = Query(..., description="City name")):
    """
    Get thunder/lightning data for a city.
    
    Args:
        city (str): City name
        
    Returns:
        ThunderResponse: Current thunder data
        
    Raises:
        HTTPException: If city not found or API error occurs
    """
    try:
        logger.info(f"Fetching thunder data for: {city}")
        data = get_thunder(city)
        return ThunderResponse(**data)
    except ValueError as e:
        logger.error(f"City not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching thunder data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching thunder data: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
