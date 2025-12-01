# SkyLink Scripts

Automation scripts for deploying and managing SkyLink services.

## Available Scripts

### start.sh / start.bat

Starts all SkyLink services with proper Docker networking.

**What it does:**
1. Creates the `skylink-network` Docker network (if not exists)
2. Starts the SkyLink API container
3. Starts the Minecraft server container

**Usage:**
```bash
# Linux/macOS
./start.sh

# Windows
.\start.bat
```

**After running:**
- API available at: `http://localhost:8080`
- Minecraft server at: `localhost:25565`

## Docker Network

Both scripts create an external Docker network called `skylink-network`. This
allows the Minecraft server container to communicate with the API container
using the hostname `skylink-api` instead of IP addresses.

**Important:** Inside Docker containers, `localhost` refers to the container
itself, not the host machine. Use container names for inter-container
communication.

## Stopping Services

```bash
# Stop individual services
docker compose -f api/docker-compose.yml down
docker compose -f papermc-mod/docker-compose.yml down

# Or stop all containers on the network
docker stop skylink-api skylink-mc-server
```

## Viewing Logs

```bash
# API logs
docker logs skylink-api

# Minecraft server logs
docker logs skylink-mc-server

# Follow logs in real-time
docker logs -f skylink-mc-server
```
