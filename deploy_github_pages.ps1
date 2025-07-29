# GitHub Pages Deployment Script (PowerShell)
# This script helps prepare and deploy the application to GitHub Pages

Write-Host "🚀 GitHub Pages Deployment Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: Not in a git repository" -ForegroundColor Red
    Write-Host "Please run this script from the root of your git repository" -ForegroundColor Yellow
    exit 1
}

# Check if required files exist
Write-Host "📋 Checking required files..." -ForegroundColor Cyan

if (-not (Test-Path "index.html")) {
    Write-Host "❌ Error: index.html not found" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "static")) {
    Write-Host "❌ Error: static directory not found" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".github/workflows/deploy.yml")) {
    Write-Host "❌ Error: GitHub Actions workflow not found" -ForegroundColor Red
    exit 1
}

Write-Host "✅ All required files found" -ForegroundColor Green

# Check git status
Write-Host ""
Write-Host "📊 Git Status:" -ForegroundColor Cyan
git status --porcelain

# Ask for confirmation
Write-Host ""
$confirmation = Read-Host "Do you want to commit and push these changes? (y/n)"

if ($confirmation -eq 'y' -or $confirmation -eq 'Y') {
    Write-Host "🔄 Committing changes..." -ForegroundColor Yellow
    
    # Add all files
    git add .
    
    # Commit with a descriptive message
    git commit -m "Add GitHub Pages deployment files

- Add static index.html for GitHub Pages
- Add GitHub Actions workflow for deployment
- Add deployment documentation
- Configure for automatic deployment to gh-pages branch"
    
    Write-Host "📤 Pushing to remote repository..." -ForegroundColor Yellow
    git push origin main
    
    Write-Host ""
    Write-Host "✅ Deployment initiated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to your repository on GitHub"
    Write-Host "2. Navigate to Settings → Pages"
    Write-Host "3. Set source to 'Deploy from a branch'"
    Write-Host "4. Select 'gh-pages' branch"
    Write-Host "5. Click Save"
    Write-Host ""
    Write-Host "🌐 Your site will be available at:" -ForegroundColor Cyan
    Write-Host "   https://yourusername.github.io/your-repo-name"
    Write-Host ""
    Write-Host "⏳ The GitHub Actions workflow will automatically deploy your site." -ForegroundColor Yellow
    Write-Host "   You can monitor progress in the Actions tab of your repository."
    
} else {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 1
} 