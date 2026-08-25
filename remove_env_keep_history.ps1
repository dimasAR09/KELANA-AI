# PowerShell script to remove .env from Git history while keeping all commits and tags

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Removing .env from Git history" -ForegroundColor Cyan
Write-Host "Keeping ALL commits and tags intact!" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "c:\Program Files\Kelana-ai"

Write-Host "Step 1: Setting environment variable..." -ForegroundColor Yellow
$env:FILTER_BRANCH_SQUELCH_WARNING = "1"

Write-Host "Step 2: Running git filter-branch..." -ForegroundColor Yellow
Write-Host "This will rewrite commits to remove backend/.env..." -ForegroundColor Yellow
Write-Host ""

git filter-branch -f --index-filter "git rm --cached --ignore-unmatch backend/.env" --prune-empty --tag-name-filter cat -- --all

Write-Host ""
Write-Host "Step 3: Cleaning up references..." -ForegroundColor Yellow
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin

Write-Host ""
Write-Host "Step 4: Running garbage collection..." -ForegroundColor Yellow
git reflog expire --expire=now --all
git gc --prune=now --aggressive

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Done! Verifying..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Commit history (should still have all commits):" -ForegroundColor Cyan
git log --oneline --all | Select-Object -First 15

Write-Host ""
Write-Host "Tags (should still have all tags):" -ForegroundColor Cyan
git tag

Write-Host ""
Write-Host "Checking if .env is in history (should be empty):" -ForegroundColor Cyan
$envHistory = git log --all --full-history -- backend/.env
if ([string]::IsNullOrEmpty($envHistory)) {
    Write-Host "✓ SUCCESS: .env removed from history!" -ForegroundColor Green
} else {
    Write-Host "✗ WARNING: .env still in history" -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Ready to push!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next step: Run push_to_github.ps1" -ForegroundColor Yellow
