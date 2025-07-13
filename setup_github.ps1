# Setup GitHub Repository Script (PowerShell)
# This script will configure your local repository for GitHub

Write-Host "🚀 Setting up GitHub repository..." -ForegroundColor Green

# Step 1: Rename branch from master to main (modern standard)
Write-Host "Step 1: Renaming branch from master to main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ Branch renamed to 'main'" -ForegroundColor Green

# Step 2: Get GitHub repository URL from user
Write-Host "Step 2: Configure GitHub remote..." -ForegroundColor Yellow
Write-Host "Please provide your GitHub repository URL." -ForegroundColor Cyan
Write-Host "Example: https://github.com/yourusername/tennis-time-blog.git" -ForegroundColor Gray

$githubUrl = Read-Host "Enter your GitHub repository URL"

if ($githubUrl) {
    # Add remote origin
    git remote add origin $githubUrl
    Write-Host "✅ Remote 'origin' added: $githubUrl" -ForegroundColor Green
    
    # Step 3: Push to GitHub
    Write-Host "Step 3: Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Your repository is now available at: $githubUrl" -ForegroundColor Cyan
    
} else {
    Write-Host "❌ No URL provided. Please run the script again with a valid GitHub URL." -ForegroundColor Red
}

Write-Host "Current Git status:" -ForegroundColor Yellow
git status
git remote -v 