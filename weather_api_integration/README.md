# Weather API Integration

Shared utility library providing geocoding and weather data access for other
SkyLink services. Also exposes a `/health` endpoint.

## Purpose

This module serves as the foundation layer for weather data:

- **Geocoding**: Convert city names to latitude/longitude coordinates
- **Weather Data**: Fetch precipitation, temperature, and sun data
- **Health Check**: Expose `/health` endpoint for API monitoring

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Returns `{"status": "ok"}` |

## Services

### geo.py

```python
from weather_api_integration.services.geo import get_lat_lon

lat, lon = get_lat_lon("London")
# Returns: (51.5074, -0.1278)
```

### weather.py

```python
from weather_api_integration.services.weather import (
    get_precipitation_data,
    get_sun_data,
    get_rain_status,
    get_thunder
)

# Get all precipitation data for a location
precip = get_precipitation_data(lat, lon)
# Returns: {"rain": 0.5, "weather_code": 61}

# Get sun position data
sun = get_sun_data(lat, lon)
# Returns: {"sunrise": "2024-01-15T07:45", "sunset": "2024-01-15T16:30"}

# Get boolean rain status
is_raining = get_rain_status(lat, lon)
# Returns: True/False

# Get thunder status from weather code
is_thunder = get_thunder(weather_code)
# Returns: True/False
```

## Standalone Usage

This service can run independently:

```bash
# Install dependencies
pip install -r ../requirements.txt

# Configure (optional)
cp .env.example .env

# Run
python main.py
```

Server runs on `http://localhost:8000` by default.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |

## External APIs Used

- **Nominatim** (OpenStreetMap): Geocoding city names
- **Open-Meteo**: Weather and sun position data

Both APIs are free and require no authentication.

## Architecture

```
weather_api_integration/
├── __init__.py
├── main.py              # Standalone FastAPI app
├── endpoints/
│   ├── __init__.py
│   └── router.py        # /health endpoint
├── services/
│   ├── __init__.py
│   ├── geo.py           # Geocoding utilities
│   └── weather.py       # Weather data utilities
├── models/
│   ├── __init__.py
│   └── health.py        # Response models
└── .env.example
```
