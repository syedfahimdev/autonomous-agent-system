#!/bin/bash

# Autonomous Multi-Agent Task Bot Deployment Script
# This script helps deploy the application to Docker or Vercel

set -e

echo "🤖 Autonomous Multi-Agent Task Bot Deployment"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check environment variables
check_env() {
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "❌ Error: OPENAI_API_KEY environment variable is not set"
        echo "Please set your OpenAI API key:"
        echo "export OPENAI_API_KEY=your_api_key_here"
        exit 1
    fi
    echo "✅ OpenAI API key is configured"
}

# Function to deploy with Docker
deploy_docker() {
    echo "🐳 Deploying with Docker..."
    
    if ! command_exists docker; then
        echo "❌ Error: Docker is not installed"
        echo "Please install Docker from https://docker.com"
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        echo "❌ Error: Docker Compose is not installed"
        echo "Please install Docker Compose"
        exit 1
    fi
    
    check_env
    
    echo "Building Docker image..."
    docker-compose build
    
    echo "Starting services..."
    docker-compose up -d
    
    echo "✅ Application deployed successfully!"
    echo "🌐 Access the dashboard at: http://localhost:8000"
    echo "📊 Health check: http://localhost:8000/api/health"
    
    echo ""
    echo "Useful commands:"
    echo "  View logs: docker-compose logs -f"
    echo "  Stop services: docker-compose down"
    echo "  Restart: docker-compose restart"
}

# Function to deploy to Vercel
deploy_vercel() {
    echo "🌐 Deploying to Vercel..."
    
    if ! command_exists vercel; then
        echo "❌ Error: Vercel CLI is not installed"
        echo "Please install Vercel CLI: npm i -g vercel"
        exit 1
    fi
    
    check_env
    
    echo "Deploying to Vercel..."
    vercel --prod
    
    echo "✅ Application deployed to Vercel!"
    echo "Don't forget to set environment variables in Vercel dashboard:"
    echo "  - OPENAI_API_KEY"
    echo "  - N8N_WEBHOOK_URL (optional)"
}

# Function to run locally
run_local() {
    echo "🚀 Running locally..."
    
    if ! command_exists python; then
        echo "❌ Error: Python is not installed"
        exit 1
    fi
    
    check_env
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    echo "Starting application..."
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  docker    Deploy using Docker Compose"
    echo "  vercel    Deploy to Vercel"
    echo "  local     Run locally with uvicorn"
    echo "  help      Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  OPENAI_API_KEY    Your OpenAI API key (required)"
    echo "  N8N_WEBHOOK_URL   n8n webhook URL (optional)"
    echo ""
    echo "Examples:"
    echo "  $0 docker"
    echo "  $0 vercel"
    echo "  $0 local"
}

# Main script logic
case "${1:-help}" in
    docker)
        deploy_docker
        ;;
    vercel)
        deploy_vercel
        ;;
    local)
        run_local
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Unknown option: $1"
        show_help
        exit 1
        ;;
esac 