@echo off
setlocal enabledelayedexpansion
title Antigravity Phone Connect - HEADLESS MODE

:: Navigate to script directory
cd /d "%~dp0"

echo ===================================================
echo   Antigravity Phone Connect - HEADLESS / REVERSE PROXY
echo ===================================================
echo.

:: 1. Ensure .env exists
if not exist ".env" (
    if exist ".env.example" (
        echo [INFO] .env file not found. Creating from .env.example...
        copy .env.example .env >nul
        echo [SUCCESS] .env created from template!
        echo [ACTION] Please open .env and configure at minimum: APP_PASSWORD, PORT
        pause
        exit /b
    ) else (
        echo [ERROR] .env.example not found. Cannot create .env template.
        pause
        exit /b
    )
)
echo [INFO] .env configuration found.

:: 2. Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js missing. Install from https://nodejs.org/
    pause
    exit /b
)

:: 3. Ensure dependencies are installed
if not exist "node_modules" (
    echo [INFO] Installing Node.js dependencies...
    call npm install
)

:: 4. Launch server directly (no Python, no ngrok)
echo [STARTING] Launching Antigravity Phone Connect (headless)...
echo (No tunnel - set up your reverse proxy / SSH tunnel externally)
echo.
node server.js

:: Keep window open if server crashes
echo.
echo [INFO] Server stopped. Press any key to exit.
pause >nul
