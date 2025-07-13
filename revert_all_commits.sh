#!/bin/bash

# Revert All Commits Script (Bash)
# This script will undo all commits and return to initial state

echo "⚠️  WARNING: This will delete ALL commits and return to initial state!"
echo "This action cannot be undone if you haven't pushed to GitHub yet."

read -p "Are you sure you want to continue? (yes/no): " confirmation

if [ "$confirmation" = "yes" ]; then
    echo "Reverting all commits..."
    
    # Option 1: Hard reset to before any commits (if you have uncommitted changes)
    git reset --hard HEAD~40
    echo "✅ Reset to 40 commits before current state"
    
    # Option 2: If the above doesn't work, reset to the very beginning
    # git reset --hard $(git rev-list --max-parents=0 HEAD)
    # echo "✅ Reset to initial commit"
    
    # Option 3: If you want to completely remove Git history
    # rm -rf .git
    # git init
    # echo "✅ Completely removed Git history and reinitialized"
    
    echo "All commits have been reverted!"
    echo "Current status:"
    git status
else
    echo "Operation cancelled."
fi 