@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Fix Secret Leak and Push to GitHub
echo Repository: https://github.com/dimasAR09/KELANA-AI
echo ============================================================
echo.
echo This script will:
echo 1. Remove .env from ALL commit history
echo 2. Keep ALL your commits intact (timestamps, messages, etc)
echo 3. Keep ALL your tags (session-2, session-3, session-4, session-5)
echo 4. Force push to GitHub with clean history
echo.
echo IMPORTANT: This is safe! All your code will be preserved.
echo Only .env file will be removed from history.
echo.
pause

cd /d "%~dp0"

echo.
echo ============================================================
echo Step 1: Remove .env from Git history
echo ============================================================
echo.

set FILTER_BRANCH_SQUELCH_WARNING=1

echo Running git filter-branch...
echo This may take a minute...
echo.

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend/.env" --prune-empty --tag-name-filter cat -- --all

if errorlevel 1 (
    echo.
    echo ERROR: Filter-branch failed. Trying alternative method...
    echo.
    
    REM Try alternative with different quote style
    git filter-branch -f --tree-filter "rm -f backend/.env" --prune-empty --tag-name-filter cat -- --all
)

echo.
echo ============================================================
echo Step 2: Clean up backup references
echo ============================================================
echo.

for /f "delims=" %%i in ('git for-each-ref --format^="delete %%%%^(refname^)" refs/original') do (
    git update-ref %%i
)

echo.
echo ============================================================
echo Step 3: Garbage collection
echo ============================================================
echo.

git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo.
echo ============================================================
echo Step 4: Verify changes
echo ============================================================
echo.

echo Commit history (all commits should still be here):
git log --oneline --all | findstr /N "^"
echo.

echo Tags (all tags should still be here):
git tag
echo.

echo Checking if .env is gone from history...
git log --all --full-history -- backend/.env > nul 2>&1
if errorlevel 1 (
    echo [OK] .env successfully removed from history!
) else (
    echo [WARNING] .env might still be in history
)

echo.
echo ============================================================
echo Step 5: Push to GitHub
echo ============================================================
echo.
echo This will FORCE PUSH to rewrite GitHub history.
echo Your commits and tags will remain, only .env will be removed.
echo.
pause

echo.
echo Pushing main branch...
git push https://github.com/dimasAR09/KELANA-AI.git main --force

echo.
echo Pushing all tags...
git push https://github.com/dimasAR09/KELANA-AI.git --tags --force

echo.
echo ============================================================
echo DONE!
echo ============================================================
echo.
echo Please verify on GitHub:
echo https://github.com/dimasAR09/KELANA-AI
echo.
echo Check:
echo [✓] All commits are there
echo [✓] All tags are there (session-2, session-3, session-4, session-5)
echo [✓] .env file is NOT visible
echo [✓] Latest commit: "Integrate Amazon Bedrock"
echo.
echo ============================================================
echo IMPORTANT: ROTATE AWS CREDENTIALS!
echo ============================================================
echo.
echo Your AWS credentials were exposed in Git history.
echo You MUST rotate them immediately:
echo.
echo 1. Login to AWS Console
echo 2. Go to IAM - Users - Security Credentials  
echo 3. Deactivate old access key
echo 4. Create new access key
echo 5. Update backend/.env with new credentials
echo.
pause
