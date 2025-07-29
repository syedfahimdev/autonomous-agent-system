# 🚀 Fly.io Deployment Guide

This guide will help you deploy your Autonomous Task Bot to Fly.io.

## Prerequisites

1. **Install Fly CLI**
   ```bash
   # macOS
   brew install flyctl
   
   # Windows
   powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
   
   # Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login to Fly.io**
   ```bash
   fly auth login
   ```

3. **Create a Fly.io account** at [fly.io](https://fly.io)

## Deployment Steps

### 1. Initialize Fly.io App

```bash
# Navigate to your project directory
cd autonomous-task-bot

# Initialize Fly.io app (if not already done)
fly launch
```

When prompted:
- **App name**: `autonomous-agent-system` (or your preferred name)
- **Region**: Choose closest to your users
- **Postgres**: No (we'll use local storage)
- **Deploy now**: No (we'll configure first)

### 2. Configure Environment Variables

```bash
# Set required environment variables
fly secrets set OPENAI_API_KEY="your-openai-api-key-here"

# Set optional environment variables
fly secrets set N8N_WEBHOOK_URL="your-n8n-webhook-url"
fly secrets set DEBUG="False"
fly secrets set HOST="0.0.0.0"
fly secrets set PORT="8000"
```

### 3. Create Persistent Volume (Optional)

```bash
# Create a volume for persistent data storage
fly volumes create autonomous_agent_data --size 1 --region iad
```

### 4. Deploy the Application

```bash
# Deploy to Fly.io
fly deploy
```

### 5. Verify Deployment

```bash
# Check app status
fly status

# View logs
fly logs

# Open the app
fly open
```

## Configuration Files

### fly.toml
The `fly.toml` file is already configured with:
- ✅ Optimized Dockerfile (`Dockerfile.fly`)
- ✅ Health checks
- ✅ Auto-scaling settings
- ✅ Persistent volume mounting
- ✅ HTTPS enforcement

### Dockerfile.fly
The Fly.io optimized Dockerfile includes:
- ✅ Better dependency resolution
- ✅ System dependencies (gcc, g++, curl)
- ✅ Upgraded pip and setuptools
- ✅ Health check configuration

## Troubleshooting

### Common Issues

1. **Dependency Conflicts**
   ```bash
   # If you encounter dependency issues, try:
   fly deploy --build-only
   ```

2. **Memory Issues**
   ```bash
   # Scale up memory if needed
   fly scale memory 2048
   ```

3. **Build Failures**
   ```bash
   # Check build logs
   fly logs --build
   
   # Rebuild from scratch
   fly deploy --build-only --no-cache
   ```

4. **Environment Variables**
   ```bash
   # List current secrets
   fly secrets list
   
   # Update secrets
   fly secrets set VARIABLE_NAME="new_value"
   ```

### Debugging Commands

```bash
# SSH into the running container
fly ssh console

# View real-time logs
fly logs --follow

# Check app health
fly status

# Scale the app
fly scale count 1

# Restart the app
fly apps restart autonomous-agent-system
```

## Performance Optimization

### 1. Auto-scaling
The app is configured to:
- ✅ Auto-start when receiving traffic
- ✅ Auto-stop when idle (cost savings)
- ✅ Minimum 0 machines running
- ✅ Health checks every 30 seconds

### 2. Resource Allocation
```bash
# Check current resources
fly status

# Scale up if needed
fly scale memory 2048
fly scale cpu 2
```

### 3. Monitoring
```bash
# View metrics
fly dashboard

# Monitor logs
fly logs --follow
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `N8N_WEBHOOK_URL` | No | n8n webhook URL for automation |
| `DEBUG` | No | Debug mode (default: False) |
| `HOST` | No | Host binding (default: 0.0.0.0) |
| `PORT` | No | Port number (default: 8000) |

## Cost Optimization

1. **Auto-stop machines**: Configured to stop when idle
2. **Shared CPU**: Using shared CPU for cost efficiency
3. **Minimal memory**: Starting with 1GB RAM
4. **No persistent storage**: Using local storage by default

## Security

- ✅ HTTPS enforced
- ✅ Environment variables encrypted
- ✅ Health checks enabled
- ✅ Auto-restart on failures

## Support

If you encounter issues:

1. **Check logs**: `fly logs`
2. **View status**: `fly status`
3. **Restart app**: `fly apps restart`
4. **Contact support**: [Fly.io Support](https://fly.io/docs/support/)

---

**Deploy with confidence! 🚀** 