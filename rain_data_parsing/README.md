# Rain Data Parsing

Microservice that provides precipitation status for Minecraft weather
synchronization. Returns whether it's currently raining or thundering at a
given location.

## Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/precipitation` | GET | Get rain/thunder status for a city |

### GET /precipitation

**Parameters:**
- `city` (required): City name (e.g., "London", "New York")

**Response:**
```json
{
  "rain": true,
  "thunder": false
}
```

**Weather Code Mapping:**
- Rain: weather codes 51-67, 80-82 (drizzle, rain, showers)
- Thunder: weather codes 95-99 (thunderstorm)

## Quick Start

### Standalone

```bash
# Install dependencies
pip install -r ../requirements.txt

# Configure (optional)
cp .env.example .env

# Run
python main.py
```

Server runs on `http://localhost:8001` by default.

### As Part of Mega-API

This service is automatically included in the combined `/api` service.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8001` | Server port |

## Architecture

```
rain_data_parsing/
├── __init__.py
├── main.py              # Standalone FastAPI app
├── endpoints/
│   ├── __init__.py
│   └── router.py        # /precipitation endpoint
├── services/
│   ├── __init__.py
│   └── precipitation.py # Weather data processing
├── models/
│   ├── __init__.py
│   └── precipitation.py # Response models
└── .env.example
```

## Dependencies

Uses `weather_api_integration` for:
- Geocoding (city → coordinates)
- Weather data fetching (coordinates → precipitation)

## How It Works

1. Receive city name from request
2. Geocode city to lat/lon via `weather_api_integration`
3. Fetch current weather code from Open-Meteo
4. Map weather code to rain/thunder booleans
5. Return JSON response
