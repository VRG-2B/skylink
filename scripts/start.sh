#!/bin/bash
# SkyLink Docker Startup Script
# Creates the shared network and launches both services

set -e

echo "=========================================="
echo "  SkyLink Docker Startup"
echo "=========================================="

# Create the shared network if it doesn't exist
echo "[1/3] Creating shared Docker network..."
docker network create skylink-network 2>/dev/null || echo "Network 'skylink-network' already exists"

# Start the API service
echo "[2/3] Starting SkyLink API..."
docker compose -f "$(dirname "$0")/../api/docker-compose.yml" up -d

# Start the Minecraft server
echo "[3/3] Starting SkyLink Minecraft Server..."
docker compose -f "$(dirname "$0")/../papermc-mod/docker-compose.yml" up -d

echo "=========================================="
echo "  SkyLink is now running!"
echo "=========================================="
echo "  API:        http://localhost:8080"
echo "  Minecraft:  localhost:25565"
echo "=========================================="
