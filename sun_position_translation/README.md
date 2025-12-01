# Sun Position Translation

Microservice that converts real-world sun position to Minecraft ticks. Returns
the current Minecraft time value based on actual sunrise/sunset times for a
given city.

## Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/time` | GET | Get Minecraft ticks for a city |

### GET /time

**Parameters:**
- `city` (required): City name (e.g., "London", "New York")

**Response:**
```json
{
  "ticks": 6000
}
```

## Minecraft Tick System

Minecraft uses a 24000-tick day cycle:

| Ticks | Time of Day | Event |
|-------|-------------|-------|
| 0 | 6:00 AM | Sunrise |
| 6000 | 12:00 PM | Noon |
| 12000 | 6:00 PM | Sunset |
| 13000 | 7:00 PM | Night begins |
| 18000 | 12:00 AM | Midnight |
| 23000 | 5:00 AM | Dawn begins |

## How Time Translation Works

Unlike simple clock-to-tick conversion, this service uses **actual sun position**:

1. **Fetch Sun Data**: Get today's sunrise/sunset times for the location
2. **Determine Period**: Is it currently day, night, or transition?
3. **Interpolate**: Map current time within that period to corresponding ticks

**Example:**
- Sunrise: 7:00 AM, Sunset: 5:00 PM (10 hour day)
- Current time: 12:00 PM (halfway through day)
- Result: 6000 ticks (Minecraft noon)

This means Minecraft noon aligns with **solar noon**, not clock noon.

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

Server runs on `http://localhost:8002` by default.

### As Part of Mega-API

This service is automatically included in the combined `/api` service.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8002` | Server port |

## Architecture

```
sun_position_translation/
├── __init__.py
├── main.py              # Standalone FastAPI app
├── endpoints/
│   ├── __init__.py
│   └── router.py        # /time endpoint
├── services/
│   ├── __init__.py
│   ├── conversion.py    # Tick calculation logic
│   └── time_service.py  # Orchestrates the conversion
├── models/
│   ├── __init__.py
│   └── time.py          # Response models
└── .env.example
```

## Dependencies

Uses `weather_api_integration` for:
- Geocoding (city → coordinates)
- Sun data fetching (coordinates → sunrise/sunset)

## Conversion Logic

```python
# Day period (sunrise to sunset)
if sunrise <= current_time <= sunset:
    progress = (current_time - sunrise) / (sunset - sunrise)
    ticks = int(progress * 12000)  # 0-12000

# Night period (sunset to next sunrise)
else:
    progress = (current_time - sunset) / (next_sunrise - sunset)
    ticks = 12000 + int(progress * 12000)  # 12000-24000
```
