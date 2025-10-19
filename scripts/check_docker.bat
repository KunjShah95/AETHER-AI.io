@echo off
REM Wrapper to run PowerShell Docker diagnostic script
SET PS1=%~dp0check_docker.ps1
echo Running Docker diagnostic (PowerShell)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
pause
