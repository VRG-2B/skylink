"""Geo service module for fetching location data."""

import requests


def get_lat_lon(city: str) -> tuple[float, float]:
    """
    Fetch latitude and longitude for a given city using Nominatim API.
    
    Args:
        city (str): City name
        
    Returns:
        tuple: (latitude, longitude)
        
    Raises:
        ValueError: If city not found
    """
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': city,
        'format': 'json',
        'limit': 1,
    }

    response = requests.get(url, params=params, headers={'User-Agent': 'skylink-weather-api'})
    data = response.json()

    if not data:
        raise ValueError(f"City '{city}' not found")

    lat = data[0]['lat']
    lon = data[0]['lon']
    return float(lat), float(lon)
