@echo off
REM AETHER-AI Installation Script for Windows
REM This script installs AETHER-AI and its dependencies

echo ========================================
echo   AETHER-AI Installation for Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [INFO] Python found. Checking version...
python --version

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python 3.9 or higher is required
    echo Please upgrade Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python version is compatible
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Git is not installed or not in PATH
    echo You can download it from https://git-scm.com/downloads
    echo Installation will continue without Git...
    set HAS_GIT=0
) else (
    echo [INFO] Git found
    git --version
    set HAS_GIT=1
)
echo.

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\AETHER-AI
echo [INFO] Installing AETHER-AI to: %INSTALL_DIR%
echo.

if exist "%INSTALL_DIR%" (
    echo [WARNING] Installation directory already exists
    echo This will update your existing installation
    echo.
    set /p CONTINUE="Continue? (Y/N): "
    if /i not "%CONTINUE%"=="Y" (
        echo Installation cancelled
        pause
        exit /b 0
    )
    echo.
) else (
    mkdir "%INSTALL_DIR%"
)

REM Clone or download the repository
cd /d "%INSTALL_DIR%"

if %HAS_GIT% EQU 1 (
    echo [INFO] Cloning repository...
    if exist ".git" (
        echo [INFO] Updating existing repository...
        git pull origin main
    ) else (
        git clone https://github.com/KunjShah95/AETHER-AI.io.git .
    )
) else (
    echo [INFO] Downloading repository archive...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/KunjShah95/AETHER-AI.io/archive/refs/heads/main.zip' -OutFile 'repo.zip'"
    powershell -Command "Expand-Archive -Path 'repo.zip' -DestinationPath '.' -Force"
    powershell -Command "Move-Item -Path 'AETHER-AI.io-main\*' -Destination '.' -Force"
    powershell -Command "Remove-Item -Path 'AETHER-AI.io-main' -Recurse -Force"
    del repo.zip
)

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download repository
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [INFO] Installing dependencies...
echo This may take several minutes...
echo.

REM Install dependencies using pyproject.toml
if exist "pyproject.toml" (
    echo [INFO] Installing from pyproject.toml...
    python -m pip install -e .
) else (
    echo [WARNING] No pyproject.toml found, installing basic dependencies...
    python -m pip install requests PyYAML rich python-dotenv google-generativeai groq ollama
)

if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Some dependencies failed to install
    echo You may need to install them manually
    echo.
)

REM Create .env file from example
echo [INFO] Setting up configuration...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env
        echo [INFO] Created .env file from template
        echo Please edit .env and add your API keys
    ) else if exist "terminal\.env.example" (
        copy terminal\.env.example .env
        echo [INFO] Created .env file from template
        echo Please edit .env and add your API keys
    )
) else (
    echo [INFO] .env file already exists
)
echo.

REM Create desktop shortcut
echo [INFO] Creating launcher script...
echo @echo off > "%INSTALL_DIR%\launch-aetherai.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\launch-aetherai.bat"
echo python terminal\main.py %%* >> "%INSTALL_DIR%\launch-aetherai.bat"

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Installation directory: %INSTALL_DIR%
echo.
echo To start AETHER-AI:
echo   1. Edit %INSTALL_DIR%\.env and add your API keys
echo   2. Run: %INSTALL_DIR%\launch-aetherai.bat
echo   Or: cd %INSTALL_DIR% ^&^& python terminal\main.py
echo.
echo To get API keys:
echo   - Gemini: https://makersuite.google.com/app/apikey
echo   - Groq: https://console.groq.com/keys
echo   - HuggingFace: https://huggingface.co/settings/tokens
echo   - OpenAI: https://platform.openai.com/api-keys
echo.
echo For more information, see README.md in the installation directory
echo.
pause
