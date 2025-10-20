@echo off
REM AetherAI Docker Quick Start for Windows
REM This script helps you get AetherAI running with Docker

echo.
echo ========================================
echo   AetherAI Docker Quick Start
echo ========================================
echo.

REM Check if Docker is installed
echo [1/5] Checking if Docker is installed...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed!
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)
echo [OK] Docker is installed
echo.

REM Check if Docker is running
echo [2/5] Checking if Docker Desktop is running...
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running!
    echo.
    echo Please start Docker Desktop and wait for it to fully start.
    echo Look for the whale icon in your system tray.
    echo.
    echo After starting Docker Desktop, run this script again.
    pause
    exit /b 1
)
echo [OK] Docker Desktop is running
echo.

REM Check if .env file exists
echo [3/5] Checking configuration...
if not exist .env (
    echo [WARNING] .env file not found!
    echo.
    echo Creating .env from .env.example...
    if exist .env.example (
        copy .env.example .env >nul
        echo [OK] .env file created
        echo.
        echo IMPORTANT: Please edit .env and add your API keys:
        echo   - GEMINI_API_KEY
        echo   - GROQ_API_KEY
        echo   - HUGGINGFACE_TOKEN
        echo   - OPENAI_API_KEY
        echo   - MCP_API_KEY
        echo.
        echo Opening .env in notepad...
        timeout /t 2 /nobreak >nul
        notepad .env
        echo.
        echo After adding your API keys, press any key to continue...
        pause >nul
    ) else (
        echo [ERROR] .env.example not found!
        pause
        exit /b 1
    )
) else (
    echo [OK] .env file exists
)
echo.

REM Build Docker image
echo [4/5] Building AetherAI Docker image...
echo This may take several minutes on first build...
echo.
docker-compose build
if errorlevel 1 (
    echo.
    echo [ERROR] Docker build failed!
    echo.
    echo Troubleshooting tips:
    echo 1. Check if you have internet connection
    echo 2. Review error messages above
    echo 3. See DOCKER_TROUBLESHOOTING.md for more help
    echo.
    pause
    exit /b 1
)
echo.
echo [OK] Docker image built successfully!
echo.

REM Start container
echo [5/5] Starting AetherAI container...
docker-compose up -d
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start container!
    echo.
    echo Try running: docker-compose logs
    pause
    exit /b 1
)
echo.
echo [OK] Container started successfully!
echo.

REM Success message
echo ========================================
echo   SUCCESS! AetherAI is now running!
echo ========================================
echo.
echo Container name: aetherai_terminal
echo.
echo To access AetherAI, run:
echo   docker exec -it aetherai_terminal python terminal/main.py
echo.
echo Or use the management script:
echo   docker-manage.bat run
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop:
echo   docker-compose down
echo.
echo For more commands, see DOCKER_QUICKSTART.md
echo.
pause
