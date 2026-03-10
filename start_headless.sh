#!/bin/bash

# Antigravity Phone Connect — Headless / Reverse Proxy mode
# Launches server directly, no Python, no ngrok.
# Suitable for systemd, crontab @reboot, or manual use.

# Navigate to script directory
cd "$(dirname "$0")"

echo "==================================================="
echo "  Antigravity Phone Connect - HEADLESS / REVERSE PROXY"
echo "==================================================="
echo

# 1. Ensure .env exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "[INFO] .env file not found. Creating from .env.example..."
        cp .env.example .env
        echo "[SUCCESS] .env created from template!"
        echo "[ACTION] Please open .env and configure at minimum: APP_PASSWORD, PORT"
        exit 0
    else
        echo "[ERROR] .env.example not found. Cannot create .env template."
        exit 1
    fi
fi
echo "[INFO] .env configuration found."

# 2. Check Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed."
    exit 1
fi

# 3. Ensure dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "[INFO] Installing Node.js dependencies..."
    npm install
fi

# 4. Load .env and export variables for Node.js
set -a
source .env
set +a

# 5. Launch server directly
echo "[STARTING] Launching Antigravity Phone Connect (headless)..."
echo "(No tunnel — set up your reverse proxy / SSH tunnel externally)"
echo
exec node server.js
