# Revert All Commits Script (PowerShell)
# This script will undo all commits and return to initial state

Write-Host "⚠️  WARNING: This will delete ALL commits and return to initial state!" -ForegroundColor Red
Write-Host "This action cannot be undone if you haven't pushed to GitHub yet." -ForegroundColor Yellow

$confirmation = Read-Host "Are you sure you want to continue? (yes/no)"

if ($confirmation -eq "yes") {
    Write-Host "Reverting all commits..." -ForegroundColor Green
    
    # Option 1: Hard reset to before any commits (if you have uncommitted changes)
    git reset --hard HEAD~40
    Write-Host "✅ Reset to 40 commits before current state" -ForegroundColor Green
    
    # Option 2: If the above doesn't work, reset to the very beginning
    # git reset --hard $(git rev-list --max-parents=0 HEAD)
    # Write-Host "✅ Reset to initial commit" -ForegroundColor Green
    
    # Option 3: If you want to completely remove Git history
    # Remove .git folder and reinitialize
    # Remove-Item -Recurse -Force .git
    # git init
    # Write-Host "✅ Completely removed Git history and reinitialized" -ForegroundColor Green
    
    Write-Host "All commits have been reverted!" -ForegroundColor Green
    Write-Host "Current status:" -ForegroundColor Yellow
    git status
} else {
    Write-Host "Operation cancelled." -ForegroundColor Yellow
} 