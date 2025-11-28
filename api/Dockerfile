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

WORKDIR /app/api

# Default environment variables
ENV HOST=0.0.0.0
ENV PORT=8080

# Run the API (uses environment variables)
CMD uvicorn main:app --host $HOST --port $PORT
