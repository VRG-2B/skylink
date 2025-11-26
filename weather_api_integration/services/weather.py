"""Weather service module with Open-Meteo API integration utilities."""

import requests
from .geo import get_lat_lon


def get_temperature(city: str) -> float:
    """
    Get current temperature for a city.
    
    Args:
        city (str): City name
        
    Returns:
        float: Current temperature in Celsius
    """
    lat, lon = get_lat_lon(city)
    
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return data['current']['temperature_2m']


def get_rain_status(city: str) -> bool:
    """
    Check if it's currently raining/snowing in a city.
    
    Args:
        city (str): City name
        
    Returns:
        bool: True if precipitation > 0
    """
    lat, lon = get_lat_lon(city)
    
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'precipitation',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return data['current']['precipitation'] > 0


def get_thunder(city: str) -> bool:
    """
    Check if there's a thunderstorm in a city.
    
    Weather codes 95-99 indicate thunderstorm.
    
    Args:
        city (str): City name
        
    Returns:
        bool: True if thunderstorm
    """
    lat, lon = get_lat_lon(city)
    
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'weather_code',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    weather_code = data['current']['weather_code']
    return 95 <= weather_code <= 99


def get_sunrise_sunset(city: str) -> tuple[str, str]:
    """
    Get sunrise and sunset times for a city.
    
    Args:
        city (str): City name
        
    Returns:
        tuple: (sunrise_time, sunset_time) as HH:MM strings
    """
    lat, lon = get_lat_lon(city)
    
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'daily': 'sunrise,sunset',
        'timezone': 'auto',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract just the time part (after 'T')
    sunrise_time = data['daily']['sunrise'][0].split('T')[1]
    sunset_time = data['daily']['sunset'][0].split('T')[1]

    return sunrise_time, sunset_time


def get_precipitation_data(city: str) -> dict:
    """
    Get precipitation (rain) and thunder status for a city.
    
    Args:
        city (str): City name
        
    Returns:
        dict: {"rain": bool, "thunder": bool}
    """
    lat, lon = get_lat_lon(city)
    
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'precipitation,weather_code',
        'timezone': 'auto',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    current_data = data.get('current', {})
    
    precipitation = current_data.get('precipitation', 0)
    rain = precipitation > 0
    
    weather_code = current_data.get('weather_code', 0)
    thunder = 95 <= weather_code <= 99
    
    return {
        'rain': rain,
        'thunder': thunder
    }


def get_sun_data(city: str) -> dict:
    """
    Get sunrise, sunset and timezone data for a city.
    
    Args:
        city (str): City name
        
    Returns:
        dict: Contains sunrise, sunset ISO strings, timezone, utc_offset_seconds
    """
    lat, lon = get_lat_lon(city)
    
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'daily': 'sunrise,sunset',
        'timezone': 'auto',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    daily = data.get('daily', {})
    
    return {
        'sunrise': daily.get('sunrise', [None])[0],
        'sunset': daily.get('sunset', [None])[0],
        'timezone': data.get('timezone', 'UTC'),
        'utc_offset_seconds': data.get('utc_offset_seconds', 0)
    }
