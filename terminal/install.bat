@echo off
title NEXUS AI Terminal Assistant - Enhanced Installer v3.0
color 0A
echo.
echo ==========================================
echo   NEXUS AI Terminal Assistant v3.0
echo   Enhanced Installation Script
echo ==========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with administrator privileges
) else (
    echo [WARNING] Not running as administrator
    echo Some features may require elevated permissions
)
echo.

REM Check if Python is installed
echo [1/6] Checking Python installation...
where python >nul 2>nul || (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check 'Add Python to PATH' during installation
    echo.
    pause
    exit /b 1
)

REM Check if pip is installed
echo [2/6] Checking pip installation...
where pip >nul 2>nul || (
    echo [ERROR] pip is not installed
    echo.
    echo Please install pip and rerun this script.
    echo.
    pause
    exit /b 1
)

REM Install dependencies
echo [3/6] Installing dependencies...
pip install -r requirements.txt

REM Copy .env.example if .env does not exist
IF NOT EXIST .env (
    copy .env.example .env
    echo .env file created. Please add your API keys.
)

echo.
echo ==========================================
echo Installation complete!
echo Run: python main.py
echo ==========================================