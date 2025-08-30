@echo off
echo 🚀 NEXUS AI Terminal - Advanced Features Setup
echo ==============================================
echo.

echo 📦 Installing advanced dependencies...
echo This may take a few minutes...
echo.

pip install --upgrade pip

pip install transformers==4.41.2
pip install torch==2.6.0
pip install accelerate==0.30.1
pip install tokenizers==0.19.1

pip install jupyter==1.0.0
pip install ipykernel==6.29.4
pip install jedi==0.19.1
pip install black==24.4.2
pip install flake8==7.0.0
pip install mypy==1.10.0
pip install autopep8==2.3.1

pip install pytest==8.2.2
pip install pytest-cov==5.0.0
pip install bandit==1.7.9
pip install safety==3.2.3
pip install radon==6.0.1

pip install psycopg2-binary==2.9.9
pip install pymongo==4.7.3
pip install sqlalchemy==2.0.31
pip install redis==5.0.7

pip install httpx==0.27.0
pip install fastapi==0.115.9
pip install uvicorn==0.30.1
pip install requests-toolbelt==1.0.0
pip install aiohttp==3.9.5

pip install gitpython==3.1.43
pip install gitdb==4.0.11

pip install memory-profiler==0.61.0
pip install line-profiler==4.1.2
pip install psutil==6.0.0

pip install astroid==3.2.2
pip install pylint==3.2.3
pip install rope==1.13.0
pip install parso==0.8.4

pip install pathlib2==2.3.7.post1
pip install watchdog==4.0.1
pip install pyyaml==6.0.1

pip install matplotlib==3.9.1
pip install plotly==5.22.0
pip install seaborn==0.13.2

pip install scikit-learn==1.5.1
pip install pandas==2.2.2
pip install numpy==1.26.4
pip install nltk==3.8.1

echo.
echo ✅ Advanced features installation complete!
echo.
echo 🎯 New features available:
echo   • Interactive Python execution
echo   • Code debugging and profiling
echo   • Unit testing and linting
echo   • API testing and database connections
echo   • Project template generation
echo   • System monitoring
echo   • Advanced Git integration
echo.
echo 🚀 Run 'python main.py' to start using the enhanced terminal!
echo.
pause
