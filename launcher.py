import sys
import subprocess
import time
import random
import string
import os
import socket
import argparse
import logging

# -----------------------------------------------------------------------------
# Dependency Management
# -----------------------------------------------------------------------------
def check_dependencies(mode='web'):
    """Checks and installs required Python packages."""
    # In 'none' mode, we only need dotenv. No ngrok/qrcode needed.
    if mode == 'none':
        needed = ["python-dotenv"]
    else:
        needed = ["pyngrok", "python-dotenv", "qrcode"]
    installed = []
    
    # Check what is missing
    for pkg in needed:
        try:
            if pkg == "pyngrok": from pyngrok import ngrok
            elif pkg == "python-dotenv": from dotenv import load_dotenv
            elif pkg == "qrcode": import qrcode
            installed.append(pkg)
        except ImportError:
            pass

    missing = [pkg for pkg in needed if pkg not in installed]
    
    if missing:
        print(f"📦 Installing missing dependencies: {', '.join(missing)}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✅ Dependencies installed.\n")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)

def check_node_environment():
    """Checks for Node.js and installs npm dependencies if needed."""
    # 1. Check if Node is installed
    try:
        subprocess.check_call(["node", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ Error: Node.js is not installed. Please install it from https://nodejs.org/")
        sys.exit(1)

    # 2. Check for node_modules
    if not os.path.exists("node_modules"):
        print("📦 'node_modules' missing. Installing Node.js dependencies...")
        try:
            # shell=True often needed on Windows for npm. On *nix, 'npm' usually works directly if in PATH.
            is_windows = sys.platform == "win32"
            subprocess.check_call(["npm", "install"], shell=is_windows)
            print("✅ Node dependencies installed.\n")
        except Exception as e:
            print(f"❌ Failed to run 'npm install': {e}")
            sys.exit(1)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def get_local_ip():
    """Robustly determines the local LAN IP address."""
    s = None
    try:
        # Connect to a public DNS server (doesn't actually send data)
        # This forces the OS to determine the correct outgoing interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_passcode():
    """Generates a 6-digit passcode."""
    return ''.join(random.choices(string.digits, k=6))

def print_qr(url):
    """Generates and prints a QR code to the terminal."""
    import qrcode
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    # Using 'ANSI' implies standard block characters which work in most terminals
    # invert=True is often needed for dark terminals (white blocks on black bg)
    qr.print_ascii(invert=True)

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Antigravity Phone Connect Launcher")
    parser.add_argument('--mode', choices=['local', 'web', 'none'], default=None,
                        help="Mode to run in: 'local' (WiFi), 'web' (Internet/ngrok), 'none' (headless, behind reverse proxy)")
    args = parser.parse_args()

    # 1. Setup Environment — load .env first to detect TUNNEL_MODE
    from dotenv import load_dotenv
    load_dotenv()

    # Auto-detect mode from TUNNEL_MODE env if not specified via CLI
    if args.mode is None:
        tunnel_env = os.environ.get('TUNNEL_MODE', '').lower()
        if tunnel_env == 'none':
            args.mode = 'none'
        elif tunnel_env == 'ngrok':
            args.mode = 'web'
        else:
            args.mode = 'web'  # Default for backward compatibility

    check_dependencies(args.mode)
    check_node_environment()
    
    # Suppress pyngrok noise (only if we'll use it)
    if args.mode == 'web':
        logging.getLogger("pyngrok").setLevel(logging.ERROR)
        from pyngrok import ngrok
    
    # Setup App Password
    passcode = os.environ.get('APP_PASSWORD')
    if not passcode:
        passcode = generate_passcode()
        os.environ['APP_PASSWORD'] = passcode # Set for child process
        print(f"⚠️  No APP_PASSWORD in .env. Using temporary: {passcode}")

    # 2. Start Node.js Server (Common to both modes)
    print(f"🚀 Starting Antigravity Server ({args.mode.upper()} mode)...")
    
    # Clean up old logs
    with open("server_log.txt", "w") as f:
        f.write(f"--- Server Started at {time.ctime()} ---\n")

    node_cmd = ["node", "server.js"]
    node_process = None
    
    try:
        # Redirect stdout/stderr to file
        log_file = open("server_log.txt", "a")
        if sys.platform == "win32":
            # On Windows, using shell=True can help with path resolution but makes killing harder.
            # We'll use shell=False and rely on PATH.
            node_process = subprocess.Popen(node_cmd, stdout=log_file, stderr=log_file, env=os.environ.copy())
        else:
            node_process = subprocess.Popen(node_cmd, stdout=log_file, stderr=log_file, env=os.environ.copy())
            
        time.sleep(2) # Give it a moment to crash if it's going to
        if node_process.poll() is not None:
            print("❌ Server failed to start immediately. Check server_log.txt.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Failed to launch node: {e}")
        sys.exit(1)

    # 3. Mode Specific Logic
    final_url = ""
    
    try:
        if args.mode == 'local':
            ip = get_local_ip()
            port = os.environ.get('PORT', '3000')
            
            # Detect HTTPS
            protocol = "http"
            if os.path.exists('certs/server.key') and os.path.exists('certs/server.cert'):
                protocol = "https"
            
            final_url = f"{protocol}://{ip}:{port}"
            
            print("\n" + "="*50)
            print(f"📡 LOCAL WIFI ACCESS")
            print("="*50)
            print(f"🔗 URL: {final_url}")
            print(f"🔑 Passcode: Not required for local WiFi (Auto-detected)")
            
            print("\n📱 Scan this QR Code to connect:")
            print_qr(final_url)

            print("-" * 50)
            print("📝 Steps to Connect:")
            print("1. Ensure your phone is on the SAME Wi-Fi network as this computer.")
            print("2. Open your phone's Camera app or a QR scanner.")
            print("3. Scan the code above OR manually type the URL into your browser.")
            print("4. You should be connected automatically!")
            
        elif args.mode == 'web':
            # Check Ngrok Token
            from pyngrok import ngrok
            token = os.environ.get('NGROK_AUTHTOKEN')
            if token:
                ngrok.set_auth_token(token)
            else:
                print("⚠️  Warning: NGROK_AUTHTOKEN not found in .env. Tunnel might expire.")

            port = os.environ.get('PORT', '3000')
            
            # Detect HTTPS
            protocol = "http"
            enable_https = os.environ.get('ENABLE_HTTPS', '').lower()
            if enable_https == 'true' or (enable_https != 'false' and os.path.exists('certs/server.key') and os.path.exists('certs/server.cert')):
                protocol = "https"
                
            addr = f"{protocol}://localhost:{port}"
            
            print("PLEASE WAIT... Establishing Tunnel...")
            tunnel = ngrok.connect(addr, host_header="rewrite")
            public_url = tunnel.public_url
            
            # Magic URL with password
            final_url = f"{public_url}?key={passcode}"
            
            print("\n" + "="*50)
            print(f"   🌍 GLOBAL WEB ACCESS")
            print("="*50)
            print(f"🔗 Base URL: {public_url}")
            print(f"🔑 Passcode: {passcode}")
            
            print("\n📱 Scan this Magic QR Code (Auto-Logins):")
            print_qr(final_url)

            print("-" * 50)
            print("📝 Steps to Connect:")
            print("1. Switch your phone to Mobile Data or Turn off Wi-Fi.")
            print("2. Open your phone's Camera app or a QR scanner.")
            print("3. Scan the code above to auto-login.")
            print(f"4. Or visit {public_url}")
            print(f"5. Enter passcode: {passcode}")
            print("6. You should be connected automatically!")

        elif args.mode == 'none':
            # Headless / Reverse Proxy mode — no tunnel, just server
            port = os.environ.get('PORT', '3000')
            external_url = os.environ.get('EXTERNAL_URL', '')
            
            # Detect protocol
            protocol = "http"
            enable_https = os.environ.get('ENABLE_HTTPS', '').lower()
            if enable_https == 'true' or (enable_https != 'false' and os.path.exists('certs/server.key') and os.path.exists('certs/server.cert')):
                protocol = "https"
            
            final_url = external_url or f"{protocol}://localhost:{port}"
            
            print("\n" + "="*50)
            print(f"   🔌 REVERSE PROXY MODE (no tunnel)")
            print("="*50)
            print(f"🔗 Local:    {protocol}://localhost:{port}")
            if external_url:
                print(f"🌍 External: {external_url}")
            print(f"🔑 Passcode: {passcode}")
            print("-" * 50)
            print("💡 Server is running. Set up your reverse proxy / SSH tunnel externally.")
            print("   Example: ssh -R 8090:localhost:{} root@your-vps".format(port))

        print("="*50)
        print("✅ Server is running in background. Logs -> server_log.txt")
        print("⌨️  Press Ctrl+C to stop.")
        
        # Keep alive loop
        last_log_pos = 0
        cdp_warning_shown = False
        
        while True:
            time.sleep(1)
            
            # Check process status
            if node_process.poll() is not None:
                print("\n❌ Server process died unexpectedly!")
                sys.exit(1)
                
            # Monitor logs for errors
            try:
                if os.path.exists("server_log.txt"):
                    with open("server_log.txt", "r", encoding='utf-8', errors='ignore') as f:
                        f.seek(last_log_pos)
                        new_lines = f.read().splitlines()
                        last_log_pos = f.tell()
                        
                        for line in new_lines:
                            if "CDP not found" in line and not cdp_warning_shown:
                                print("\n" + "!"*50)
                                print("❌ ERROR: Antigravity Editor Not Detected!")
                                print("!"*50)
                                print("   The server cannot see your editor.")
                                print("   1. Close Antigravity.")
                                print("   2. Re-open it with the debug flag:")
                                print("      antigravity . --remote-debugging-port=9000")
                                print("   3. Or use the 'Open with Antigravity (Debug)' context menu.")
                                print("!"*50 + "\n")
                                cdp_warning_shown = True
            except Exception:
                pass

    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Cleanup
        try:
            if node_process:
                node_process.terminate()
                try:
                    node_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    node_process.kill()
            
            if args.mode == 'web':
                from pyngrok import ngrok as ngrok_mod
                ngrok_mod.kill()
        except:
            pass
        
        if 'log_file' in locals() and log_file:
            log_file.close()
        
        sys.exit(0)

if __name__ == "__main__":
    main()
