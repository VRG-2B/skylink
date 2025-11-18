"""Weather service module for fetching weather data."""

import requests


def get_lat_lon(city):
    """
    Fetch latitude and longitude for a given city using Nominatim API.
    
    Args:
        city (str): City name
        
    Returns:
        tuple: (latitude, longitude)
    """
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': city,
        'format': 'json',
        'limit': 1,
    }

    response = requests.get(url, params=params, headers={'User-Agent': 'city-lat-lon-script'})
    data = response.json()

    if not data:
        raise ValueError(f"City '{city}' not found")

    lat = data[0]['lat']
    lon = data[0]['lon']
    return float(lat), float(lon)


def get_thunder(city):
    """
    Fetch current thunder/lightning probability data for a given city.
    
    Args:
        city (str): City name
        
    Returns:
        dict: Thunder data including lightning probability
    """
    lat, lon = get_lat_lon(city)
    
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'lightning_probability',
        'timezone': 'auto',
    }

    response = requests.get(url, params=params)
    data = response.json()

    current_data = data.get('current', {})
    
    thunder_info = {
        'city': city,
        'latitude': lat,
        'longitude': lon,
        'lightning_probability': current_data.get('lightning_probability', 0),
        'timezone': data.get('timezone', 'UTC'),
        'time': current_data.get('time', 'N/A')
    }
    
    return thunder_info
