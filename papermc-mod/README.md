# SkyLink PaperMC Plugin

A PaperMC plugin that synchronizes Minecraft weather and time with real-world
conditions by polling the SkyLink API.

## Features

- **Automatic Weather Sync**: Rain and thunder match real-world conditions
- **Real Sun Position**: Time reflects actual sunrise/sunset for your city
- **In-Game Commands**: Change city, check status, control syncing
- **Game Rule Management**: Automatically disables vanilla day/night and weather cycles
- **Configurable Polling**: Set sync interval to balance accuracy vs. API calls

## Requirements

- PaperMC 1.21+
- Java 21+
- SkyLink API running (see [api/](../api/README.md))

## Installation

### Docker (Recommended)

Use the root `scripts/start.bat` or `scripts/start.sh` to launch both the API
and Minecraft server with proper networking.

### Manual Installation

1. Build the plugin:
```bash
./gradlew build
```

2. Copy the JAR to your server:
```bash
cp build/libs/skylink-*.jar /path/to/server/plugins/
```

3. Configure `plugins/SkyLink/config.yml`:
```yaml
api:
  host: "localhost"  # or "skylink-api" for Docker
  port: 8080

sync:
  interval_seconds: 120
  enabled: true

location:
  city: "London"
```

4. Start your server

## Commands

| Command | Permission | Description |
|---------|------------|-------------|
| `/skylink city [name]` | `skylink.use` | View or set the synced city |
| `/skylink status` | `skylink.use` | View sync status and API health |
| `/skylink sync` | `skylink.admin` | Force an immediate weather sync |
| `/skylink start` | `skylink.admin` | Start the weather sync service |
| `/skylink stop` | `skylink.admin` | Stop the weather sync service |

## Permissions

| Permission | Default | Description |
|------------|---------|-------------|
| `skylink.use` | `true` | Basic commands (city, status) |
| `skylink.admin` | `op` | Admin commands (sync, start, stop) |

## Configuration

### config.yml

```yaml
api:
  host: "skylink-api"      # API hostname (container name for Docker)
  port: 8080               # API port

sync:
  interval_seconds: 120    # Sync every 2 minutes
  enabled: true            # Enable automatic syncing

location:
  city: "London"           # Default city to sync
```

### Environment Variables

Configuration can also be set via environment variables (takes precedence):

| Variable | Config Key | Description |
|----------|------------|-------------|
| `SKYLINK_API_HOST` | `api.host` | API hostname |
| `SKYLINK_API_PORT` | `api.port` | API port |
| `SKYLINK_SYNC_INTERVAL` | `sync.interval_seconds` | Sync interval |
| `SKYLINK_SYNC_ENABLED` | `sync.enabled` | Enable syncing |
| `SKYLINK_CITY` | `location.city` | Default city |

## How It Works

1. **On Enable**: Plugin disables `doDaylightCycle` and `doWeatherCycle` game rules
2. **Polling**: Every N seconds, fetches `/time` and `/precipitation` from API
3. **Apply**: Sets world time and weather based on API response
4. **On Disable**: Re-enables vanilla game rules

## Architecture

```
papermc-mod/
├── src/main/java/skylink/
│   ├── SkyLink.java                    # Main plugin class
│   ├── domain/config/
│   │   └── PluginConfig.java           # Configuration management
│   └── infrastructure/
│       ├── api/
│       │   └── SkyLinkApiClient.java   # HTTP client for API
│       ├── commands/
│       │   ├── SkyLinkCommand.java     # Command handler
│       │   └── location/
│       │       └── CityCommand.java    # City subcommand
│       └── sync/
│           └── WeatherSyncService.java # Scheduler service
├── src/main/resources/
│   ├── config.yml                      # Default configuration
│   └── plugin.yml                      # Plugin metadata
├── build.gradle.kts                    # Gradle build config
├── Dockerfile                          # Container build
└── docker-compose.yml                  # Container deployment
```

## Building

```bash
# Build the plugin JAR
./gradlew build  # Only if you've generated your Gradle wrapper yet

# Output: build/libs/skylink-1.0.0-beta.jar
```

## Docker Networking

When running in Docker, use the container name `skylink-api` as the host, not
`localhost` or `127.0.0.1`. Docker containers have isolated network namespaces,
so `localhost` inside the MC container refers to itself, not the API container.

## Troubleshooting

**API errors in status:**
- Verify API container is running
- Check hostname is `skylink-api` (not `localhost`) in Docker
- Test API directly: `curl http://localhost:8080/health`

**Weather not updating:**
- Run `/skylink status` to check last sync time
- Check server logs for API errors
- Try `/skylink sync` to force update

**Time seems wrong:**
- Time is based on actual sun position, not clock time
- Solar noon varies by location and date
- Try a different city to verify

## Dependencies

- PaperMC API 1.21
- Gson (included via shadow plugin)
- OkHttp (included via shadow plugin)
