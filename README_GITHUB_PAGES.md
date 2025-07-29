# GitHub Pages Deployment Guide

This guide explains how to deploy the Autonomous Multi-Agent Task Bot to GitHub Pages.

## Overview

This repository contains a FastAPI backend application and a static frontend that can be deployed to GitHub Pages. The static frontend (`index.html`) works in two modes:

1. **Demo Mode**: Works without a backend, showing simulated results
2. **Connected Mode**: Connects to a deployed backend API

## Quick Deployment

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Choose **gh-pages** branch
5. Click **Save**

### 2. Push to Main Branch

The GitHub Actions workflow will automatically:
- Deploy the static files to the `gh-pages` branch
- Make your site available at `https://yourusername.github.io/your-repo-name`

## File Structure for GitHub Pages

```
├── index.html              # Main static page
├── static/                 # Static assets
│   ├── styles.css         # CSS styles
│   ├── favicon.ico        # Favicon
│   └── favicon.svg        # SVG favicon
├── .github/workflows/     # GitHub Actions
│   └── deploy.yml         # Deployment workflow
└── README_GITHUB_PAGES.md # This file
```

## Backend Deployment Options

To connect the frontend to a real backend, deploy your FastAPI application to one of these services:

### Option 1: Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Option 2: Render
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option 3: Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### Option 4: Heroku
```bash
# Install Heroku CLI
# Create Procfile with: web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Deploy
heroku create your-app-name
git push heroku main
```

## Connecting Frontend to Backend

1. Deploy your backend using one of the options above
2. Get your backend URL (e.g., `https://your-app.railway.app`)
3. In the GitHub Pages site, enter your backend URL in the API Configuration section
4. Click "Update Configuration"

## API Endpoints Required

Your backend must provide these endpoints:

- `POST /api/tasks` - Submit tasks
- `GET /api/tasks` - Get task history  
- `GET /api/health` - Health check

## Demo Mode

If no backend URL is provided, the site runs in demo mode:
- Shows simulated task processing
- Displays example results
- No real AI processing occurs
- Perfect for testing the interface

## Customization

### Styling
Edit `static/styles.css` to customize the appearance.

### Configuration
Modify the JavaScript in `index.html` to:
- Change default settings
- Add new task types
- Customize demo responses

## Troubleshooting

### Common Issues

1. **Site not loading**: Check that GitHub Pages is enabled and the `gh-pages` branch exists
2. **CORS errors**: Ensure your backend allows requests from your GitHub Pages domain
3. **API connection fails**: Verify your backend URL is correct and the service is running

### Debug Steps

1. Check browser console for JavaScript errors
2. Verify API endpoints are accessible
3. Test backend health endpoint manually
4. Check GitHub Actions logs for deployment issues

## Security Notes

- The frontend runs entirely in the browser
- No sensitive data is stored on GitHub Pages
- API keys should only be stored on your backend
- Use HTTPS for all API communications

## Support

For issues with:
- **GitHub Pages**: Check GitHub documentation
- **Backend deployment**: Refer to your chosen platform's docs
- **Application logic**: Check the main README.md

## License

This project is licensed under the same terms as the main repository. 