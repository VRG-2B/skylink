"""
Weather API Integration Service.
Provides /health endpoint and shared geo utilities.
"""

import sys
import os

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
