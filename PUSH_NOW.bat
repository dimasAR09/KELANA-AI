@echo off
echo ============================================================
echo Pushing to GitHub: https://github.com/dimasAR09/KELANA-AI
echo ============================================================
echo.

cd /d "%~dp0"

echo Step 1: Show current status
git status
echo.
echo ============================================================
echo.

echo Step 2: Pushing commits to GitHub...
git push https://github.com/dimasAR09/KELANA-AI.git main
echo.

if errorlevel 1 (
    echo [INFO] Trying alternative push method...
    git push origin main
    echo.
)

echo.
echo ============================================================
echo.

echo Step 3: Pushing tag session-5...
git push https://github.com/dimasAR09/KELANA-AI.git session-5 --force
echo.

if errorlevel 1 (
    echo [INFO] Trying alternative tag push...
    git push origin session-5 --force
    echo.
)

echo.
echo ============================================================
echo Step 4: Verification
echo ============================================================
echo.

echo Local commits:
git log --oneline -5
echo.

echo Current status:
git status
echo.

echo ============================================================
echo DONE!
echo ============================================================
echo.
echo Please check your GitHub repository:
echo https://github.com/dimasAR09/KELANA-AI
echo.
echo You should see:
echo - Latest commit: "Integrate Amazon Bedrock"
echo - Tag: session-5
echo.
pause
