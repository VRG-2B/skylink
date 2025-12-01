# SkyLink API

The combined API service that aggregates all SkyLink endpoints into a single
FastAPI application. This is the recommended deployment for the Minecraft plugin.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/time` | GET | Get Minecraft ticks for a city |
| `/precipitation` | GET | Get rain/thunder status for a city |

## Quick Start

### Docker (Recommended)

```bash
docker compose up -d
```

The API will be available at `http://localhost:8080`.

### Local Development

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env as needed
```

3. Run the server:
```bash
python main.py
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8080` | Server port |

### Docker Networking

When running with Docker, this service joins the `skylink-network` to communicate
with the Minecraft server container. The API is accessible to other containers
via the hostname `skylink-api`.

## API Reference

### GET /health

Returns API health status.

**Response:**
```json
{"status": "ok"}
```

### GET /time

Returns current Minecraft ticks based on real sun position for a city.

**Parameters:**
- `city` (required): City name (e.g., "London", "New York")

**Response:**
```json
{"ticks": 6000}
```

**Tick Reference:**
- `0` - Sunrise
- `6000` - Noon
- `12000` - Sunset
- `18000` - Midnight

### GET /precipitation

Returns current rain and thunder status for a city.

**Parameters:**
- `city` (required): City name

**Response:**
```json
{"rain": true, "thunder": false}
```

## Architecture

This service aggregates routers from:
- `weather_api_integration` - Health endpoint and shared utilities
- `rain_data_parsing` - Precipitation endpoint
- `sun_position_translation` - Time endpoint

```
api/
├── main.py           # FastAPI application entry point
├── router.py         # Aggregates all service routers
├── Dockerfile        # Container build configuration
├── docker-compose.yml
└── .env.example      # Environment template
```

## Dependencies

- FastAPI
- Uvicorn
- python-dotenv
- Pydantic

See `../requirements.txt` for full dependency list.
