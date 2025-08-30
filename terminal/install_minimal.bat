@echo off
echo 🚀 NEXUS AI Terminal - Minimal Installation
echo ==========================================
echo.

echo 📦 Installing core dependencies first...
echo.

pip install --upgrade pip

echo Installing basic packages...
pip install google-generativeai==0.8.3
pip install groq==0.9.0
pip install ollama==0.3.1
pip install python-dotenv==1.0.1
pip install rich==13.7.1
pip install requests==2.32.3
pip install PyYAML==6.0.1

echo.
echo Installing development tools...
pip install jedi==0.19.1
pip install black==24.4.2
pip install autopep8==2.3.1

echo.
echo Installing testing framework...
pip install pytest==8.2.2

echo.
echo Installing database connectors...
pip install psycopg2-binary==2.9.9
pip install pymongo==4.7.3
pip install redis==5.0.7

echo.
echo Installing web/API tools...
pip install httpx==0.27.0
pip install fastapi==0.115.9
pip install uvicorn==0.30.1

echo.
echo Installing Git tools...
pip install GitPython==3.1.43

echo.
echo Installing system monitoring...
pip install psutil==6.0.0

echo.
echo Installing data processing...
pip install pandas==2.2.2
pip install numpy==1.26.4

echo.
echo Installing security tools...
pip install cryptography==42.0.8

echo.
echo ✅ Core installation complete!
echo.
echo 🎯 Your NEXUS AI Terminal is ready with basic features!
echo.
echo 🚀 Run 'python main.py' to start using the terminal!
echo.
echo 💡 To install advanced features later, run: install_advanced.bat
echo.
pause
