"""
Skylink Mega API.
Combines all service endpoints into a single API.

Endpoints:
- GET /health - Health check
- GET /precipitation?city={city} - Rain and thunder status
- GET /time?city={city} - Current Minecraft ticks
"""

import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add workspace root to path for package imports
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

from fastapi import FastAPI

from router import api_router

app = FastAPI(
    title="Skylink API",
    description="Minecraft-friendly weather control API",
    version="1.0.0"
)

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host=host, port=port)
