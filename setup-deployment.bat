@echo off
REM IMPERIAL HOUSE - Automated Deployment Setup
REM This script prepares the app for deployment to Render

echo.
echo ======================================
echo  IMPERIAL HOUSE - Deployment Setup
echo ======================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    echo After installing Git, run this script again.
    pause
    exit /b 1
)

echo [1/5] Git is installed ✓
echo.

REM Initialize git repository
if not exist .git (
    echo [2/5] Initializing Git repository...
    git init
    git config user.name "Imperial House Developer"
    git config user.email "developer@imperialhouse.ke"
    echo       Git initialized ✓
) else (
    echo [2/5] Git repository already exists ✓
)
echo.

REM Remove unnecessary files from git
echo [3/5] Configuring .gitignore...
if not exist .gitignore (
    echo instance/ > .gitignore
    echo __pycache__/ >> .gitignore
    echo *.pyc >> .gitignore
    echo .env >> .gitignore
    echo .venv/ >> .gitignore
    echo venv/ >> .gitignore
    echo app/static/uploads/* >> .gitignore
    echo !app/static/uploads/.gitkeep >> .gitignore
    echo *.db >> .gitignore
    echo .DS_Store >> .gitignore
    echo .idea/ >> .gitignore
    echo .vscode/ >> .gitignore
    echo *.swp >> .gitignore
)
echo       .gitignore configured ✓
echo.

REM Add all files
echo [4/5] Adding files to Git...
git add .
git status
echo       Files added ✓
echo.

REM Create first commit
echo [5/5] Creating initial commit...
git commit -m "Initial commit: IMPERIAL HOUSE rental platform"
echo       Commit created ✓
echo.

echo ======================================
echo  Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Create GitHub account: https://github.com/signup
echo 2. Create new repository called "imperial-house"
echo 3. Run this command to push your code:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/imperial-house.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. Then deploy on Render.com
echo.
pause
