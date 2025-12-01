# SkyLink - Real-World Weather Synchronization for Minecraft

SkyLink is a Minecraft server plugin that synchronizes in-game weather and time
with real-world conditions. Choose any city in the world, and watch as your
Minecraft server's sky reflects actual sunrise times, rainfall, and storms.

Built for PaperMC servers, SkyLink combines a modular Python API backend with a
Java plugin frontend to bring realistic atmospheric conditions to your Minecraft
world.

## Project Philosophy

SkyLink follows the "run it yourself" philosophy. By deploying your own instance,
you get:

- **Complete Privacy** - Location data never leaves your infrastructure
- **Full Control** - Customize sync intervals, weather behavior, and more
- **No Dependencies** - No external services beyond free weather and location APIs

## Features

- **Real-Time Weather Sync**: Automatically syncs Minecraft weather with real-world conditions
- **Accurate Sun Position**: Minecraft time reflects actual sunrise/sunset times for your city
- **Thunder & Rain Detection**: Real precipitation data triggers in-game weather events
- **City-Based Location**: Simply set a city name - no coordinates needed
- **Configurable Sync Interval**: Control how often weather updates (default: 2 minutes)
- **Docker Ready**: Complete containerized deployment with shared networking
- **Modular Architecture**: Standalone microservices that can run independently or combined

## Quick Start

### Docker Deployment (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/VRG-2B/skylink.git
cd skylink
```

2. Run the startup script:
```bash
# Windows
.\scripts\start.bat

# Linux/macOS
./scripts/start.sh
```

3. Connect to your Minecraft server at `localhost:25565`

4. Set your city in-game:
```
/skylink city London
```

### Manual Deployment

See individual service READMEs for standalone deployment:
- [API Service](./api/README.md)
- [PaperMC Plugin](./papermc-mod/README.md)

## Architecture

```
skylink/
├── api/                        # Combined mega-API service
├── weather_api_integration/    # Shared weather utilities
├── rain_data_parsing/          # Precipitation endpoint service
├── sun_position_translation/   # Time/ticks endpoint service
├── papermc-mod/                # Minecraft plugin (Java)
└── scripts/                    # Deployment automation
```

| Directory | Description |
|-----------|-------------|
| `api/` | Combined FastAPI service aggregating all endpoints |
| `weather_api_integration/` | Shared utilities for geocoding and weather APIs |
| `rain_data_parsing/` | Standalone precipitation service |
| `sun_position_translation/` | Standalone time translation service |
| `papermc-mod/` | PaperMC plugin source code |
| `scripts/` | Docker startup scripts |

### API Endpoints

| Endpoint | Description | Response |
|----------|-------------|----------|
| `GET /health` | Health check | `{"status": "ok"}` |
| `GET /time?city={city}` | Current Minecraft ticks | `{"ticks": 6000}` |
| `GET /precipitation?city={city}` | Rain/thunder status | `{"rain": true, "thunder": false}` |

### How It Works

1. **Geocoding**: City name → latitude/longitude via Nominatim API
2. **Weather Data**: Coordinates → weather data via Open-Meteo API
3. **Time Translation**: Real sunrise/sunset → Minecraft ticks (0-24000)
4. **Plugin Sync**: Java plugin polls API and applies weather/time to world

## Configuration

### Plugin (`config.yml`)
```yaml
api:
  host: "skylink-api"  # Container name for Docker networking
  port: 8080

sync:
  interval_seconds: 120
  enabled: true

location:
  city: "London"
```

### Environment Variables

Each service supports `.env` configuration:
```env
HOST=0.0.0.0
PORT=8080
```

## In-Game Commands

| Command | Permission | Description |
|---------|------------|-------------|
| `/skylink status` | `skylink.use` | View sync status and API health |
| `/skylink city [name]` | `skylink.admin` | View or set synced city |
| `/skylink sync` | `skylink.admin` | Force immediate weather sync |
| `/skylink start` | `skylink.admin` | Start weather syncing |
| `/skylink stop` | `skylink.admin` | Stop weather syncing |

## Development

### Prerequisites

- **API**: Python 3.11+, pip
- **Plugin**: Java 21+, Gradle 8+
- **Deployment**: Docker, Docker Compose

### Building from Source

```bash
# API
pip install -r requirements.txt
python -m api.main

# Plugin
cd papermc-mod
./gradlew build  # Only if you've generated your Gradle wrapper yet
```

## Troubleshooting

### Common Issues

**Plugin shows API errors:**
- Ensure API container is running: `docker ps`
- Check API health: `curl http://localhost:8080/health`
- Verify `config.yml` uses API's container name, not `localhost` or something similar

**Weather not syncing:**
- Check sync is enabled: `/skylink status`
- Verify city is valid: try a major city like "London"
- Check PaperMC server logs for API errors

**Time seems wrong:**
- Time is based on real sunrise/sunset, not your local clock (to get accurate sun position)
- Noon (12:00 local) ≠ 6000 ticks; it depends on real sun position

## External APIs

SkyLink uses these free, no-auth-required APIs:
- [Open-Meteo](https://open-meteo.com/) - Weather data
- [Nominatim](https://nominatim.org/) - Geocoding

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following existing architecture
4. Submit a pull request

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

Built with passion for immersive Minecraft experiences. Sync your world with reality!
