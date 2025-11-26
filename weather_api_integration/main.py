"""
Weather API Integration Service.
Provides /health endpoint and shared geo utilities.
"""

import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add workspace root to path
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from fastapi import FastAPI

from weather_api_integration.endpoints.router import router

app = FastAPI(title="Weather API Integration", version="1.0.0")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
