#!/bin/bash

# GitHub Pages Deployment Script
# This script helps prepare and deploy the application to GitHub Pages

echo "🚀 GitHub Pages Deployment Script"
echo "================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "Please run this script from the root of your git repository"
    exit 1
fi

# Check if required files exist
echo "📋 Checking required files..."

if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found"
    exit 1
fi

if [ ! -d "static" ]; then
    echo "❌ Error: static directory not found"
    exit 1
fi

if [ ! -f ".github/workflows/deploy.yml" ]; then
    echo "❌ Error: GitHub Actions workflow not found"
    exit 1
fi

echo "✅ All required files found"

# Check git status
echo ""
echo "📊 Git Status:"
git status --porcelain

# Ask for confirmation
echo ""
read -p "Do you want to commit and push these changes? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Committing changes..."
    
    # Add all files
    git add .
    
    # Commit with a descriptive message
    git commit -m "Add GitHub Pages deployment files
    
    - Add static index.html for GitHub Pages
    - Add GitHub Actions workflow for deployment
    - Add deployment documentation
    - Configure for automatic deployment to gh-pages branch"
    
    echo "📤 Pushing to remote repository..."
    git push origin main
    
    echo ""
    echo "✅ Deployment initiated!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Go to your repository on GitHub"
    echo "2. Navigate to Settings → Pages"
    echo "3. Set source to 'Deploy from a branch'"
    echo "4. Select 'gh-pages' branch"
    echo "5. Click Save"
    echo ""
    echo "🌐 Your site will be available at:"
    echo "   https://yourusername.github.io/your-repo-name"
    echo ""
    echo "⏳ The GitHub Actions workflow will automatically deploy your site."
    echo "   You can monitor progress in the Actions tab of your repository."
    
else
    echo "❌ Deployment cancelled"
    exit 1
fi 