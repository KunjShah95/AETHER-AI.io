@echo off
REM aetherai launcher - runs the installed console script or falls back to python -m terminal.main
where aetherai >nul 2>&1
if %ERRORLEVEL% == 0 (
    aetherai %*
    goto :eof
)

REM Fallback: run via python -m
python -m terminal.main %*
