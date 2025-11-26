"""Precipitation service module for fetching rain and thunder data."""

import sys
import os

# Add workspace root to path for importing weather_api_integration
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from weather_api_integration.services.weather import get_precipitation_data


def get_precipitation(city: str) -> dict:
    """
    Fetch current precipitation (rain and thunder) data for a given city.
    
    Args:
        city (str): City name
        
    Returns:
        dict: {"rain": bool, "thunder": bool}
    """
    return get_precipitation_data(city)
