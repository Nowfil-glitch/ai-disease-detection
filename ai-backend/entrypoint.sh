#!/bin/bash
set -e

# Run model setup to ensure models are present
# This is now handled during the Docker build phase, but we keep it here
# as a fallback if someone runs the container without pre-built models
# or if they mount a volume over /app/models
# echo "Setting up AI models..."
# python create_demo_models.py

# Start the application
# Use the PORT environment variable if available (for Render)
PORT=${PORT:-8000}
echo "Starting server on port $PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
