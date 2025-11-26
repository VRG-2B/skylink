"""Time service for fetching current Minecraft ticks based on city location."""

import sys
import os
from datetime import datetime, timezone, timedelta

# Add workspace root to path for importing weather_api_integration
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from weather_api_integration.services.weather import get_sun_data
from .conversion import iso_to_time, interpolate_ticks


def get_current_ticks(city: str) -> int:
    """
    Get current Minecraft ticks for a city based on sunrise, sunset, and current time.
    
    Args:
        city (str): City name
        
    Returns:
        int: Current Minecraft ticks (0-23999)
    """
    # Get sun data from shared weather service
    sun_data = get_sun_data(city)
    
    sunrise_iso = sun_data['sunrise']
    sunset_iso = sun_data['sunset']
    utc_offset_seconds = sun_data['utc_offset_seconds']
    
    if not sunrise_iso or not sunset_iso:
        raise ValueError("Could not get sunrise/sunset data")
    
    # Parse sunrise and sunset times
    sunrise_time = iso_to_time(sunrise_iso)
    sunset_time = iso_to_time(sunset_iso)
    
    # Get current time in the city's timezone
    tz_offset = timezone(timedelta(seconds=utc_offset_seconds))
    current_datetime = datetime.now(tz_offset)
    current_time = current_datetime.time()
    
    # Interpolate to get Minecraft ticks
    ticks = interpolate_ticks(sunrise_time, sunset_time, current_time)
    
    return ticks
