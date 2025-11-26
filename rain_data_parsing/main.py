"""
Rain Data Parsing Service.
Provides /precipitation endpoint for rain and thunder data.
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

from rain_data_parsing.endpoints.router import router

app = FastAPI(title="Rain Data Parsing API", version="1.0.0")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host=host, port=port)
