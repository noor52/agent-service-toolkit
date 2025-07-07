#!/usr/bin/env python3
"""
AI Agent Service Toolkit - Setup Fix Script
This script helps diagnose and fix common setup issues.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ ERROR: Python 3.11 or higher is required!")
        print("Please install Python 3.11+ from https://python.org/downloads/")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required API keys."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ ERROR: .env file not found!")
        print("Creating .env file from .env.example...")
        
        example_path = Path(".env.example")
        if example_path.exists():
            # Copy .env.example to .env
            with open(example_path, 'r') as src, open(env_path, 'w') as dst:
                dst.write(src.read())
            print("✓ Created .env file from .env.example")
        else:
            # Create basic .env file
            with open(env_path, 'w') as f:
                f.write("# Add your API keys here\n")
                f.write("OPENAI_API_KEY=\n")
                f.write("ANTHROPIC_API_KEY=\n")
                f.write("GOOGLE_API_KEY=\n")
                f.write("GROQ_API_KEY=\n")
                f.write("USE_FAKE_MODEL=true\n")
            print("✓ Created basic .env file")
    
    # Check for API keys
    api_keys_found = []
    with open(env_path, 'r') as f:
        content = f.read()
        
    key_patterns = [
        "OPENAI_API_KEY=",
        "ANTHROPIC_API_KEY=", 
        "GOOGLE_API_KEY=",
        "GROQ_API_KEY=",
        "USE_FAKE_MODEL=true"
    ]
    
    for pattern in key_patterns:
        if pattern in content:
            line = [line for line in content.split('\n') if line.startswith(pattern)][0]
            if '=' in line and line.split('=', 1)[1].strip():
                api_keys_found.append(pattern.replace('=', ''))
    
    if not api_keys_found:
        print("⚠️  WARNING: No API keys found in .env file!")
        print("Adding USE_FAKE_MODEL=true for testing...")
        
        # Add fake model setting
        with open(env_path, 'a') as f:
            f.write("\n# Temporary setting for testing\n")
            f.write("USE_FAKE_MODEL=true\n")
        
        print("✓ Added fake model setting for testing")
        return True
    else:
        print(f"✓ Found API keys: {', '.join(api_keys_found)}")
        return True

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    try:
        # Try to install uv first
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], 
                      check=True, capture_output=True)
        print("✓ Installed uv package manager")
        
        # Install project dependencies with uv
        result = subprocess.run(["uv", "sync", "--frozen"], 
                              check=True, capture_output=True, text=True)
        print("✓ Installed project dependencies with uv")
        
    except subprocess.CalledProcessError as e:
        print("⚠️  uv installation failed, trying with pip...")
        try:
            # Fallback to pip
            subprocess.run([sys.executable, "-m", "pip", "install", "."], 
                          check=True, capture_output=True)
            print("✓ Installed dependencies with pip")
        except subprocess.CalledProcessError as e2:
            print(f"❌ ERROR: Failed to install dependencies: {e2}")
            return False
    
    return True

def check_ports():
    """Check if required ports are available."""
    import socket
    
    ports_to_check = [8080, 8501]
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"⚠️  WARNING: Port {port} is already in use!")
            print(f"   You may need to stop other services or change the port.")
        else:
            print(f"✓ Port {port} is available")

def create_startup_scripts():
    """Create convenient startup scripts."""
    
    # Windows batch script
    windows_script = """@echo off
echo Starting AI Agent Service Toolkit...
echo.

echo Activating virtual environment...
call .venv\\Scripts\\activate.bat

echo Starting FastAPI service...
start "FastAPI Service" cmd /k "python src\\run_service.py"

echo Waiting for service to start...
timeout /t 5 /nobreak > nul

echo Starting Streamlit app...
start "Streamlit App" cmd /k "streamlit run src\\streamlit_app.py"

echo.
echo Services are starting...
echo FastAPI service: http://localhost:8080
echo Streamlit app: http://localhost:8501
echo.
pause
"""
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "Starting AI Agent Service Toolkit..."
echo

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Starting FastAPI service in background..."
python src/run_service.py &
SERVICE_PID=$!

echo "Waiting for service to start..."
sleep 5

echo "Starting Streamlit app..."
streamlit run src/streamlit_app.py &
APP_PID=$!

echo
echo "Services are running:"
echo "FastAPI service: http://localhost:8080"
echo "Streamlit app: http://localhost:8501"
echo
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $SERVICE_PID $APP_PID; exit" INT
wait
"""
    
    # Write scripts
    with open("start_windows.bat", "w") as f:
        f.write(windows_script)
    
    with open("start_unix.sh", "w") as f:
        f.write(unix_script)
    
    # Make unix script executable
    try:
        os.chmod("start_unix.sh", 0o755)
    except:
        pass
    
    print("✓ Created startup scripts:")
    print("  - start_windows.bat (for Windows)")
    print("  - start_unix.sh (for macOS/Linux)")

def main():
    """Main setup fix function."""
    print("🔧 AI Agent Service Toolkit - Setup Fix Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check and fix .env file
    if not check_env_file():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check ports
    check_ports()
    
    # Create startup scripts
    create_startup_scripts()
    
    print("\n" + "=" * 50)
    print("🎉 Setup fix completed!")
    print("\nNext steps:")
    print("1. Run the startup script for your OS:")
    print("   - Windows: double-click start_windows.bat")
    print("   - macOS/Linux: ./start_unix.sh")
    print("2. Or run manually:")
    print("   - Terminal 1: python src/run_service.py")
    print("   - Terminal 2: streamlit run src/streamlit_app.py")
    print("3. Open http://localhost:8501 in your browser")
    
    return True

if __name__ == "__main__":
    main()