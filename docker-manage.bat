@echo off
REM NEXUS AI Docker Management Script for Windows

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="build" goto build
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="logs" goto logs
if "%1"=="shell" goto shell
if "%1"=="run" goto run
if "%1"=="clean" goto clean
if "%1"=="test" goto test
if "%1"=="rebuild" goto rebuild
goto help

:help
echo.
echo AetherAI Docker Management
echo ==========================
echo.
echo Available commands:
echo   docker-manage.bat build       - Build Docker image
echo   docker-manage.bat up          - Start containers in detached mode
echo   docker-manage.bat down        - Stop and remove containers
echo   docker-manage.bat logs        - View container logs
echo   docker-manage.bat shell       - Open shell in running container
echo   docker-manage.bat run         - Run the application interactively
echo   docker-manage.bat clean       - Remove containers, volumes, and images
echo   docker-manage.bat test        - Test Docker image
echo   docker-manage.bat rebuild     - Clean and rebuild everything
echo.
goto end

:build
echo Building AetherAI Docker image...
docker-compose build --no-cache
goto end

:up
echo Starting AetherAI containers...
docker-compose up -d
echo Containers started! Use 'docker-manage.bat logs' to view output
goto end

:down
echo Stopping AetherAI containers...
docker-compose down
goto end

:logs
docker-compose logs -f
goto end

:shell
docker exec -it aetherai_terminal /bin/bash
goto end

:run
docker exec -it aetherai_terminal python terminal/main.py
goto end

:clean
echo Cleaning up Docker resources...
docker-compose down -v --rmi all
echo Cleanup complete!
goto end

:test
echo Testing AetherAI Docker image...
docker-compose run --rm aetherai python -c "import sys; print(f'Python {sys.version}'); sys.exit(0)"
echo Test passed!
goto end

:rebuild
call :clean
call :build
call :up
goto end

:end
