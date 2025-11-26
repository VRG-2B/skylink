"""
Rain Data Parsing Service.
Provides /precipitation endpoint for rain and thunder data.
"""

import sys
import os

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
    uvicorn.run(app, host="0.0.0.0", port=8001)
