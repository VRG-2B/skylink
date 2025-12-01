@echo off
REM SkyLink Docker Startup Script
REM Creates the shared network and launches both services

echo ==========================================
echo   SkyLink Docker Startup
echo ==========================================

REM Create the shared network if it doesn't exist
echo [1/3] Creating shared Docker network...
docker network create skylink-network 2>nul || echo Network 'skylink-network' already exists

REM Start the API service
echo [2/3] Starting SkyLink API...
docker compose -f "%~dp0..\api\docker-compose.yml" up -d

REM Start the Minecraft server
echo [3/3] Starting SkyLink Minecraft Server...
docker compose -f "%~dp0..\papermc-mod\docker-compose.yml" up -d

echo ==========================================
echo   SkyLink is now running!
echo ==========================================
echo   API:        http://localhost:8080
echo   Minecraft:  localhost:25565
echo ==========================================
