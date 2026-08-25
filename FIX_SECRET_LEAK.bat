@echo off
echo ============================================================
echo FIX: Remove .env from Git History
echo ============================================================
echo.
echo IMPORTANT: This will rewrite Git history to remove AWS credentials
echo that were accidentally committed in the past.
echo.
pause

cd /d "%~dp0"

echo.
echo Step 1: Remove .env from entire Git history...
echo.

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend/.env" --prune-empty --tag-name-filter cat -- --all

echo.
echo ============================================================
echo.

echo Step 2: Clean up backup refs...
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin

echo.
echo Step 3: Garbage collect...
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo.
echo ============================================================
echo.

echo Step 4: Force push to GitHub...
echo This will rewrite history on GitHub (safe, just removing secrets)
echo.
pause

git push origin main --force
git push origin session-5 --force

echo.
echo ============================================================
echo DONE!
echo ============================================================
echo.
echo The .env file has been removed from Git history.
echo Your AWS credentials are now safe.
echo.
echo IMPORTANT: You should also rotate your AWS credentials
echo since they were exposed in Git history!
echo.
pause
