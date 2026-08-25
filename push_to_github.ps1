# PowerShell script to push to GitHub

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Pushing to GitHub" -ForegroundColor Cyan
Write-Host "Repository: https://github.com/dimasAR09/KELANA-AI" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "c:\Program Files\Kelana-ai"

Write-Host "Current status:" -ForegroundColor Yellow
git status
Write-Host ""

Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "Pushing to GitHub (force push required to rewrite history)" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to continue with force push"

Write-Host ""
Write-Host "Pushing main branch..." -ForegroundColor Yellow
git push origin main --force

Write-Host ""
Write-Host "Pushing all tags..." -ForegroundColor Yellow
git push origin --tags --force

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Done!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Verification:" -ForegroundColor Cyan
Write-Host "1. Go to: https://github.com/dimasAR09/KELANA-AI" -ForegroundColor Cyan
Write-Host "2. Check commits are all there" -ForegroundColor Cyan
Write-Host "3. Check tags (session-2, session-3, session-4, session-5)" -ForegroundColor Cyan
Write-Host "4. Check .env is NOT visible in any commit" -ForegroundColor Cyan
Write-Host ""

Write-Host "IMPORTANT: Rotate your AWS credentials!" -ForegroundColor Red
Write-Host "Old credentials were exposed in Git history." -ForegroundColor Red
Write-Host ""

Read-Host "Press Enter to exit"
