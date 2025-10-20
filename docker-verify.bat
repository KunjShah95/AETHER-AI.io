@echo off
echo Checking Docker installation and status...
echo.

echo 1. Checking Docker version:
docker --version
if errorlevel 1 (
    echo [ERROR] Docker is not installed or not in PATH
    goto end
)
echo.

echo 2. Checking Docker Compose version:
docker-compose --version
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed
    goto end
)
echo.

echo 3. Checking if Docker daemon is running:
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Desktop is not running!
    echo.
    echo Please start Docker Desktop and try again.
    echo Look for the whale icon in your system tray.
    goto end
)
echo [SUCCESS] Docker daemon is running!
echo.

echo 4. Testing Docker with hello-world:
docker run --rm hello-world
echo.

echo [SUCCESS] Docker is properly configured!
echo You can now run: docker-compose build
echo.

:end
pause
