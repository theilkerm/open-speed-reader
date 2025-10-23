@echo off
echo Speed Reader - Installation and Launch Script
echo ============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
    echo.
)

REM Run the application
echo Starting Speed Reader...
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
