"""Combined router aggregating all service routers."""

import sys
import os

# Base path (workspace root)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add workspace root to path so we can import service packages
if base_path not in sys.path:
    sys.path.insert(0, base_path)

from fastapi import APIRouter

# Import routers from each service package
from weather_api_integration.endpoints.router import router as weather_router
from rain_data_parsing.endpoints.router import router as rain_router
from sun_position_translation.endpoints.router import router as sun_router

# Create main API router
api_router = APIRouter()

api_router.include_router(weather_router)
api_router.include_router(rain_router)
api_router.include_router(sun_router)
