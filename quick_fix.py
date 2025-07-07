#!/usr/bin/env python3
"""
Quick fix for missing langchain dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Quick Fix for Missing Dependencies")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("src/run_service.py").exists():
        print("❌ Error: Please run this script from the project root directory")
        return False
    
    # Step 1: Create .env file if missing
    if not Path(".env").exists():
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("USE_FAKE_MODEL=true\n")
        print("✅ Created .env file with fake model")
    
    # Step 2: Install uv if not available
    print("🔧 Installing uv package manager...")
    run_command(f"{sys.executable} -m pip install uv", "Installing uv")
    
    # Step 3: Install all dependencies
    print("📦 Installing project dependencies...")
    if not run_command("uv sync --frozen", "Installing with uv"):
        print("⚠️  uv failed, trying alternative method...")
        # Alternative: install specific missing packages
        packages = [
            "langchain-anthropic",
            "langchain-openai", 
            "langchain-google-genai",
            "langchain-groq",
            "langchain-community",
            "langchain-core",
            "langgraph",
            "fastapi",
            "streamlit",
            "uvicorn",
            "httpx",
            "pydantic",
            "python-dotenv"
        ]
        
        for package in packages:
            run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}")
    
    # Step 4: Try to run a quick test
    print("\n🧪 Testing import...")
    try:
        # Test the problematic import
        subprocess.run([sys.executable, "-c", "from langchain_anthropic import ChatAnthropic; print('✅ Import successful')"], 
                      check=True, capture_output=True)
        print("✅ Dependencies are working!")
    except subprocess.CalledProcessError:
        print("⚠️  Still having import issues, trying pip install...")
        run_command(f"{sys.executable} -m pip install langchain-anthropic", "Installing langchain-anthropic with pip")
    
    print("\n" + "=" * 40)
    print("🎉 Fix completed! Try running the service now:")
    print("   python src/run_service.py")
    
    return True

if __name__ == "__main__":
    main()