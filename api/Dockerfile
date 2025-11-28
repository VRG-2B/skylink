# SkyLink API Dockerfile
FROM python:3.11-slim

# Set up working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (context is workspace root)
COPY api/ ./api/
COPY rain_data_parsing/ ./rain_data_parsing/
COPY sun_position_translation/ ./sun_position_translation/
COPY weather_api_integration/ ./weather_api_integration/

# Set PYTHONPATH so modules can be found
ENV PYTHONPATH=/app

WORKDIR /app/api

# Default environment variables
ENV HOST=0.0.0.0
ENV PORT=8080

# Run the API (uses environment variables)
CMD uvicorn main:app --host $HOST --port $PORT
