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
        echo [ACTION] Please open .env and configure: APP_PASSWORD, SSH_HOST, PORT etc.
        pause
        exit /b
    ) else (
        echo [ERROR] .env.example not found.
        pause
        exit /b
    )
)
echo [INFO] .env configuration found.

:: 2. Read .env variables
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
    set "line=%%A"
    if not "!line:~0,1!"=="#" (
        if not "%%B"=="" (
            set "%%A=%%B"
        )
    )
)

:: 3. Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js missing. Install from https://nodejs.org/
    pause
    exit /b
)

:: 4. Ensure dependencies are installed
if not exist "node_modules" (
    echo [INFO] Installing Node.js dependencies...
    call npm install
)

:: 5. Check SSH config and start tunnel
if not defined SSH_HOST (
    echo [WARNING] SSH_HOST not set in .env. Skipping SSH tunnel.
    echo           Set SSH_HOST, SSH_USER, SSH_REMOTE_PORT to enable auto-tunnel.
) else (
    if not defined SSH_USER set SSH_USER=root
    if not defined SSH_REMOTE_PORT set SSH_REMOTE_PORT=8090
    if not defined PORT set PORT=3443

    echo [SSH] Starting reverse tunnel: %SSH_USER%@%SSH_HOST% -R %SSH_REMOTE_PORT%:127.0.0.1:%PORT%
    start "SSH Tunnel" ssh -N -o "ServerAliveInterval=30" -o "ServerAliveCountMax=3" -R %SSH_REMOTE_PORT%:127.0.0.1:%PORT% %SSH_USER%@%SSH_HOST%
    echo [SSH] Tunnel started in background window.
    timeout /t 2 /nobreak >nul
)

:: 6. Launch server
echo.
echo [STARTING] Launching Antigravity Phone Connect...
echo (Press Ctrl+C in this window to stop the server)
echo.
node server.js

:: Keep window open if server crashes
echo.
echo [INFO] Server stopped. Press any key to exit.
pause >nul
