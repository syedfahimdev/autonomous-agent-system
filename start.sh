#!/bin/bash

# Startup script for Autonomous Task Bot
# Created by Syed Fahim

set -e

echo "🚀 Starting Autonomous Task Bot..."

# Create necessary directories
mkdir -p /app/data/memory /app/data/reports /app/static /app/templates

# Check if environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
fi

# Start the application
echo "📡 Starting uvicorn server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 