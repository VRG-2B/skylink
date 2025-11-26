"""
Sun Position Translation Service.
Provides /time endpoint for Minecraft ticks based on city location.
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

from sun_position_translation.endpoints.router import router

app = FastAPI(title="Sun Position Translation API", version="1.0.0")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8002"))
    uvicorn.run(app, host=host, port=port)
