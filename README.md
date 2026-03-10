<div align="center">
  <img src="./assets/antigravity.png" alt="Antigravity Phone Connect" width="300">
  <h1>Antigravity Phone Connect 📱</h1>
</div>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Antigravity Phone Connect** is a high-performance, real-time mobile monitor and remote control for your Antigravity AI sessions. It allows you to step away from your desk while keeping full sight and control over your AI's thinking process and generations.

![Antigravity Phone Connect](./assets/global_access_hero_2.png)

**Note:** This project is a refined fork/extension based on the original [Antigravity Shit-Chat](https://github.com/gherghett/Antigravity-Shit-Chat) by gherghett.

---

## 🚀 Quick Start

> 💡 **Tip:** While we recommend starting Antigravity first, the server is now smart enough to wait and automatically connect whenever Antigravity becomes available!

### Step 1: Launch Antigravity in Debug Mode

Start Antigravity with the remote debugging port enabled:

**Option A: Using Right-Click Context Menu (Recommended)**
- Run `install_context_menu.bat` (Windows) or `./install_context_menu.sh` (Linux) and select **[1] Install**
- Then right-click any project folder → **"Open with Antigravity (Debug)"** (now with visual icons!)

**Option B: Manual Command**
```bash
antigravity . --remote-debugging-port=9000
```

### Step 2: Open or Start a Chat

- In Antigravity, open an **existing chat** from the bottom-right panel, **OR**
- Start a **new chat** by typing a message

> 💡 The server needs an active chat session to capture snapshots. Without this, you'll see "chat container not found" errors.

### Step 3: Run the Server

**Windows:**
```
Double-click start_ag_phone_connect.bat
```

**macOS / Linux:**
```bash
chmod +x start_ag_phone_connect.sh   # First time only
./start_ag_phone_connect.sh
```

The script will:
- Verify Node.js and Python dependencies
- Auto-kill any existing server on port 3000
- **Wait for Antigravity** if it's not started yet
- Display a **QR Code** and your **Link** (e.g., `https://192.168.1.5:3000`)
- Provide numbered steps for easy connection

### Step 4: Connect Your Phone (Local Wi-Fi)

1. Ensure your phone is on the **same Wi-Fi network** as your PC
2. Open your mobile browser and enter the **URL shown in the terminal**
3. If using HTTPS: Accept the self-signed certificate warning on first visit

---

## 🌍 NEW: Global Remote Access (Web Mode)

Access your Antigravity session from **anywhere in the world** (Mobile Data, outside Wi-Fi) with secure passcode protection.

### Setup (First Time)
1. **Get an ngrok Token**: Sign up for free at [ngrok.com](https://ngrok.com) and get your "Authtoken".
2. **Automatic Configuration (Recommended)**: Simply run any launcher script. They will detect if `.env` is missing and automatically create it using `.env.example` as a template.
3. **Manual Setup**: Alternatively, copy `.env.example` to `.env` manually and update the values:
   ```bash
   copy .env.example .env   # Windows
   cp .env.example .env     # Mac/Linux
   ```
   Update the `.env` file with your details:
   ```env
   NGROK_AUTHTOKEN=your_token_here
   APP_PASSWORD=your_secure_passcode
   XXX_API_KEY=your-ai-provider-key
   PORT=3000
   ```

### Usage
- **Windows**: Run `start_ag_phone_connect_web.bat`
- **Mac/Linux**: Run `./start_ag_phone_connect_web.sh`

The script will launch the server and provide a **Public URL** (e.g., `https://abcd-123.ngrok-free.app`). 

**Two Ways to Connect:**
1. **Magic Link (Easiest)**: Scan the **Magic QR Code** displayed in the terminal. It logs you in automatically!
2. **Manual**: 
   - Open the URL on your phone.
   - Enter your `APP_PASSWORD` to log in.

> 💡 **Tip:** Devices on the same local Wi-Fi still enjoy direct access without needing a password.

---

## 🔒 Enabling HTTPS (Recommended)

For a secure connection without the browser warning icon:

### Option 1: Command Line
```bash
node generate_ssl.js
```
- Uses **OpenSSL** if available (includes your IP in certificate)
- Falls back to **Node.js crypto** if OpenSSL not found
- Creates certificates in `./certs/` directory

### Option 2: Web UI
1. Start the server on HTTP
2. Look for the yellow **"⚠️ Not Secure"** banner
3. Click **"Enable HTTPS"** button
4. Restart the server when prompted

### After Generating:
1. **Restart the server** - it will automatically detect and use HTTPS.
2. **On your phone's first visit**:
   - You'll see a security warning (normal for self-signed certs).
   - Tap **"Advanced"** → **"Proceed to site"**.
   - The warning won't appear again!

---

### macOS: Adding Right-Click "Quick Action" (Optional)

Since macOS requires Automator for context menu entries, follow these steps manually:

1.  Open **Automator** (Spotlight → type "Automator").
2.  Click **File → New** and select **Quick Action**.
3.  At the top, set:
    - "Workflow receives current" → **folders**
    - "in" → **Finder**
4.  In the left sidebar, search for **"Run Shell Script"** and drag it to the right pane.
5.  Set "Shell" to `/bin/zsh` and "Pass input" to **as arguments**.
6.  Paste this script:
    ```bash
    cd "$1"
    antigravity . --remote-debugging-port=9000
    ```
7.  **Save** the Quick Action with a name like `Open with Antigravity (Debug)`.
8.  Now you can right-click any folder in Finder → **Quick Actions → Open with Antigravity (Debug)**.

---

## 🏗️ Architecture Infographic

![Repo Infographic](./assets/repo_infographic.png)

---

## 🛡️ Shielding & Account Safety

This tool is designed with a **"Local-First"** security model. 

- **Bridge Mechanism**: It uses the **Chrome DevTools Protocol (CDP)** to mirror the UI of your *already-running* desktop session. It **never** extracts OAuth tokens or interacts with Google/AI-provider APIs directly.
- **Natural Traffic**: All AI requests are still sent by your official desktop application. To the AI provider, your usage looks identical to normal desktop activity.
- **Zero Bans**: There have been **no reports** of account flags or bans. This is a "Wireless Viewport," not a third-party client that bypasses official security.

---

## ✨ Features

- **🧹 Clean Mobile View (NEW!)**: Automatically filters out "Review Changes" bars, "Linked Objects," and Desktop-specific input areas to keep your phone view focused purely on the chat and code content.
- **Glassmorphism UI (NEW!)**: Sleek and modern quick-action and settings menus featuring a beautiful glassmorphism effect for enhanced mobile usability. Includes customizable, ready-to-use prompt pills (like "Explain this code", "Continue", and "Fix Bugs").
- **🌙 Improved Dark Mode (NEW!)**: Enhanced UI styling and state capture designed to provide maximum clarity and correct model detection in dark mode.
- **🧠 Latest AI Models**: Automatically updated support for the latest model versions from Gemini, Claude, and OpenAI.
- **📜 Premium Chat History (NEW!)**: Full-screen history management with a completely redesigned, sleek card-based UI. Features modern loading states, gorgeous gradients, and intelligent strictly-scoped scraping to safely extract past conversations without background noise. Dismissing the history view automatically triggers a remote Escape sequence on the desktop to keep your workspace clean.
- **➕ One-Tap New Chat (NEW!)**: Start a fresh conversation instantly from your phone without needing to touch your desktop.
- **🖼️ Context Menu Icons (NEW!)**: Visual icons in the right-click menu for better navigation.
- **🌍 Global Web Access**: Secure remote access via ngrok tunnel. Access your AI from mobile data with passcode protection.
- **🛡️ Auto-Cleanup**: Launchers now automatically sweep away "ghost" processes from previous sessions for a clean start every time.
- **🔒 HTTPS Support**: Secure connections with self-signed SSL certificates.
- **Local Image Support**: Local images and SVGs (`vscode-file://` paths) in the desktop chat are automatically converted to Base64 so they render perfectly on mobile without exposing local files.
- **Real-Time Mirroring**: 1-second polling interval for near-instant sync.
- **Remote Control**: Send messages, stop generations, and switch Modes (Fast/Planning) or Models (Gemini/Claude/GPT) directly from your phone.
- **Scroll Sync**: When you scroll on your phone, the desktop Antigravity scrolls too!
- **🎯 Precision Remote Control (NEW!)**: A deterministic targeting layer that prevents "Sync-Fighting". It uses leaf-node filtering to ensure clicks land exactly on buttons, even when nested inside complex DOM structures.
- **Occurrence Index Tracking**: Robustly handles multiple identical elements (like three "Run" buttons in history) by tracking the specific tapped instance.
- **Thought Expansion**: Tap on "Thinking..." or "Thought" blocks on your phone to remotely expand/collapse them with first-line text matching.
- **Smart Sync**: Bi-directional synchronization ensures your phone always shows the current Model and Mode selected on your desktop.
- **Premium Mobile UI**: A sleek, dark-themed interface optimized for touch interaction.
- **Context Menu Management**: Dedicated scripts to **Install, Remove, Restart, or Backup** your Right-Click integrations.
- **Health Monitoring**: Built-in `/health` endpoint for server status checks.
- **Graceful Shutdown**: Clean exit on Ctrl+C, closing all connections properly.
- **Zero-Config**: The launch scripts handle the heavy lifting of environment setup.

---

## 🔌 Deployment: Caddy + SSH Reverse Proxy (Stable Domain)

If you have your own VPS, you can deploy Phone Connect behind a **Caddy reverse proxy** with an **SSH tunnel** instead of ngrok. This gives you a **stable domain** (no random URLs) with automatic Let's Encrypt HTTPS.

### Architecture

```text
Phone (mobile network)
    │ HTTPS (Let's Encrypt)
    ▼
ag.your-domain.com  (Caddy on VPS)
    │ reverse_proxy
    ▼
host.docker.internal:8090  (VPS)
    │  SSH Reverse Tunnel
    ▼
localhost:3443  (Home PC, Phone Connect)
    │ CDP
    ▼
Antigravity IDE  (Home PC, debug mode)
```

### Step 1: Configure `.env` on your home PC

```env
APP_PASSWORD=your-secure-passcode
PORT=3443
TUNNEL_MODE=none
ENABLE_HTTPS=false
TRUST_PROXY=true
EXTERNAL_URL=https://ag.your-domain.com
SESSION_SECRET=your-random-secret-here
AUTH_SALT=your-random-salt-here
# SESSION_TTL_HOURS=720   # 30 days (default)
```

> 💡 `ENABLE_HTTPS=false` because TLS is handled by Caddy. `TRUST_PROXY=true` ensures the server sees real client IPs.

### Step 2: Start Phone Connect

```bash
# Windows
start_headless.bat

# Linux/macOS
./start_headless.sh

# Or directly:
node server.js
```

### Step 3: SSH Reverse Tunnel

```bash
# One-shot:
ssh -R 8090:localhost:3443 root@your-vps

# Persistent (recommended):
autossh -M 0 -f -N \
  -o "ServerAliveInterval 30" \
  -o "ServerAliveCountMax 3" \
  -R 8090:localhost:3443 root@your-vps
```

> ⚠️ Ensure `GatewayPorts yes` is set in your VPS `sshd_config` if Caddy runs in Docker.

### Step 4: Caddy Config on VPS

**Option A: Phone Connect serves HTTP** (recommended — simpler, TLS only at Caddy):

```caddyfile
ag.your-domain.com {
    # Optional: extra auth layer at proxy level
    # basic_auth {
    #     user $2a$14$hashed_password
    # }

    reverse_proxy host.docker.internal:8090
}
```

**Option B: Phone Connect serves HTTPS** (self-signed):

```caddyfile
ag.your-domain.com {
    reverse_proxy host.docker.internal:8090 {
        transport http {
            tls
            tls_insecure_skip_verify
        }
    }
}
```

### Step 5: systemd Service (optional, Linux)

```ini
# /etc/systemd/system/ag-phone-connect.service
[Unit]
Description=Antigravity Phone Connect
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/user/antigravity_phone_chat
ExecStart=/usr/bin/node server.js
EnvironmentFile=/home/user/antigravity_phone_chat/.env
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now ag-phone-connect
```

### Usage

1. Open `https://ag.your-domain.com` on your phone
2. Enter your `APP_PASSWORD` (first time) — session cookie lasts 30 days by default
3. Subsequent visits: you're already logged in, just open the URL

---

## 📋 CHANGELOG (Reverse Proxy / Stable Domain Support)

### New Environment Variables

| Variable | Default | Description |
|---|---|---|
| `TUNNEL_MODE` | `ngrok` | `none` = no tunnel (reverse proxy mode), `ngrok` = original behavior |
| `ENABLE_HTTPS` | auto | `true` / `false` / auto-detect from `certs/` |
| `SSL_KEY_PATH` | `./certs/server.key` | Custom path to SSL private key |
| `SSL_CERT_PATH` | `./certs/server.cert` | Custom path to SSL certificate |
| `TRUST_PROXY` | `false` | Set to `true` when behind a reverse proxy |
| `EXTERNAL_URL` | — | Your stable external URL (for diagnostics) |
| `SESSION_TTL_HOURS` | `720` (30d) | Cookie session lifetime in hours |
| `PASSCODE` | — | Alias for `APP_PASSWORD` |

### Behavioral Changes

- **`TUNNEL_MODE=none`**: The ngrok browser-warning header is no longer sent. No ngrok dependencies required.
- **`TRUST_PROXY=true`**: Express `trust proxy` is enabled — `req.ip` reflects the real client IP from `X-Forwarded-For`.
- **`ENABLE_HTTPS=false`**: Forces HTTP even when SSL certificates exist in `./certs/`.
- **Cookie improvements**: Added `sameSite: 'lax'` for better cross-site security.
- **Startup banner**: Server now logs active configuration (tunnel mode, HTTPS, TTL, external URL) at startup.
- **`/health` endpoint**: Now includes `tunnelMode`, `trustProxy`, `externalUrl`, `sessionTtlHours`.

### New Files

| File | Purpose |
|---|---|
| `start_headless.bat` | Windows: start server directly (no Python, no ngrok) |
| `start_headless.sh` | Linux/macOS: start server directly, sources `.env` |

### Backward Compatibility

- All existing behavior is preserved when `TUNNEL_MODE=ngrok` (default).
- `APP_PASSWORD` still works; `PASSCODE` is just an alias.
- Existing `start_ag_phone_connect.bat/sh` and `start_ag_phone_connect_web.bat/sh` work unchanged.

---

## 📂 Documentation

For more technical details, check out:
- [**Code Documentation**](CODE_DOCUMENTATION.md) - Architecture, Data Flow, and API.
- [**Security Guide**](SECURITY.md) - HTTPS setup, certificate warnings, and security model.
- [**Design Philosophy**](DESIGN_PHILOSOPHY.md) - Why it was built this way.
- [**Contributing**](CONTRIBUTING.md) - Guidelines for developers.

---

## License

Licensed under the [GNU GPL v3](LICENSE).  
Copyright (C) 2026 **Krishna Kanth B** (@krishnakanthb13)

---

## Star History

<a href="https://www.star-history.com/#krishnakanthb13/antigravity_phone_chat&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=krishnakanthb13/antigravity_phone_chat&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=krishnakanthb13/antigravity_phone_chat&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=krishnakanthb13/antigravity_phone_chat&type=date&legend=top-left" />
 </picture>
</a>

---

