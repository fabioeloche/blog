#!/bin/bash

# Setup GitHub Repository Script (Bash)
# This script will configure your local repository for GitHub

echo "🚀 Setting up GitHub repository..."

# Step 1: Rename branch from master to main (modern standard)
echo "Step 1: Renaming branch from master to main..."
git branch -M main
echo "✅ Branch renamed to 'main'"

# Step 2: Get GitHub repository URL from user
echo "Step 2: Configure GitHub remote..."
echo "Please provide your GitHub repository URL."
echo "Example: https://github.com/yourusername/tennis-time-blog.git"

read -p "Enter your GitHub repository URL: " githubUrl

if [ -n "$githubUrl" ]; then
    # Add remote origin
    git remote add origin "$githubUrl"
    echo "✅ Remote 'origin' added: $githubUrl"
    
    # Step 3: Push to GitHub
    echo "Step 3: Pushing to GitHub..."
    git push -u origin main
    
    echo "✅ Successfully pushed to GitHub!"
    echo "Your repository is now available at: $githubUrl"
    
else
    echo "❌ No URL provided. Please run the script again with a valid GitHub URL."
fi

echo "Current Git status:"
git status
git remote -v 