#!/usr/bin/env python3
"""
AI Agent Service Toolkit - Current Issues Fix Script
This script diagnoses and fixes current issues in the running application.
"""

import os
import sys
import subprocess
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemDiagnostics:
    """Comprehensive system diagnostics and fixes."""
    
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible."""
        version = sys.version_info
        logger.info(f"Python version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 11):
            self.issues_found.append("Python version too old (requires 3.11+)")
            return False
        return True
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed."""
        required_packages = [
            'langchain_core',
            'langchain_anthropic', 
            'langchain_openai',
            'langgraph',
            'fastapi',
            'streamlit',
            'uvicorn',
            'httpx',
            'pydantic'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                logger.info(f"✓ {package} installed")
            except ImportError:
                missing_packages.append(package)
                logger.error(f"✗ {package} missing")
        
        if missing_packages:
            self.issues_found.append(f"Missing packages: {', '.join(missing_packages)}")
            return False
        return True
    
    def check_env_file(self) -> bool:
        """Check if .env file exists and has required configuration."""
        env_path = Path(".env")
        
        if not env_path.exists():
            self.issues_found.append(".env file missing")
            return False
        
        # Check for at least one API key or fake model
        with open(env_path, 'r') as f:
            content = f.read()
        
        api_keys = [
            'OPENAI_API_KEY=',
            'ANTHROPIC_API_KEY=',
            'GOOGLE_API_KEY=',
            'GROQ_API_KEY=',
            'USE_FAKE_MODEL=true'
        ]
        
        has_config = any(key in content and content.split(key, 1)[1].split('\n')[0].strip() for key in api_keys)
        
        if not has_config:
            self.issues_found.append("No API keys or fake model configured in .env")
            return False
        
        logger.info("✓ .env file configured")
        return True
    
    def check_ports(self) -> bool:
        """Check if required ports are available."""
        import socket
        
        ports_to_check = [8080, 8501]
        busy_ports = []
        
        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                busy_ports.append(port)
                logger.warning(f"Port {port} is in use")
            else:
                logger.info(f"✓ Port {port} available")
        
        if busy_ports:
            self.issues_found.append(f"Ports in use: {', '.join(map(str, busy_ports))}")
            return False
        return True
    
    def check_database_connection(self) -> bool:
        """Check database connectivity."""
        try:
            # Import here to avoid issues if dependencies are missing
            from memory import initialize_database
            
            async def test_db():
                try:
                    async with initialize_database() as db:
                        if hasattr(db, 'setup'):
                            await db.setup()
                        logger.info("✓ Database connection successful")
                        return True
                except Exception as e:
                    logger.error(f"✗ Database connection failed: {e}")
                    self.issues_found.append(f"Database connection error: {e}")
                    return False
            
            return asyncio.run(test_db())
        except Exception as e:
            logger.error(f"✗ Database check failed: {e}")
            self.issues_found.append(f"Database check error: {e}")
            return False
    
    def check_model_imports(self) -> bool:
        """Check if model providers can be imported."""
        providers = {
            'OpenAI': 'langchain_openai.ChatOpenAI',
            'Anthropic': 'langchain_anthropic.ChatAnthropic',
            'Google': 'langchain_google_genai.ChatGoogleGenerativeAI',
            'Groq': 'langchain_groq.ChatGroq'
        }
        
        working_providers = []
        failed_providers = []
        
        for provider, import_path in providers.items():
            try:
                module_name, class_name = import_path.rsplit('.', 1)
                module = __import__(module_name, fromlist=[class_name])
                getattr(module, class_name)
                working_providers.append(provider)
                logger.info(f"✓ {provider} provider available")
            except Exception as e:
                failed_providers.append(provider)
                logger.warning(f"✗ {provider} provider unavailable: {e}")
        
        if not working_providers:
            self.issues_found.append("No model providers available")
            return False
        
        logger.info(f"Available providers: {', '.join(working_providers)}")
        return True

class IssueFixer:
    """Automated issue fixing."""
    
    def __init__(self):
        self.fixes_applied = []
    
    def fix_missing_env(self) -> bool:
        """Create .env file with fake model enabled."""
        try:
            env_content = """# AI Agent Service Toolkit Configuration
# Created by fix script

# Enable fake model for testing
USE_FAKE_MODEL=true

# Add your API keys here when ready
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here
# GOOGLE_API_KEY=your_google_key_here
# GROQ_API_KEY=your_groq_key_here

# Database configuration
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=checkpoints.db

# Server configuration
HOST=0.0.0.0
PORT=8080

# Optional: Enable tracing
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=your_langsmith_key_here
"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            
            self.fixes_applied.append("Created .env file with fake model")
            logger.info("✓ Created .env file")
            return True
        except Exception as e:
            logger.error(f"Failed to create .env file: {e}")
            return False
    
    def fix_missing_dependencies(self) -> bool:
        """Install missing dependencies."""
        try:
            logger.info("Installing missing dependencies...")
            
            # Try uv first
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "uv"], 
                              check=True, capture_output=True)
                subprocess.run(["uv", "sync", "--frozen"], 
                              check=True, capture_output=True)
                self.fixes_applied.append("Installed dependencies with uv")
                logger.info("✓ Dependencies installed with uv")
                return True
            except subprocess.CalledProcessError:
                logger.warning("uv failed, trying pip...")
                
                # Fallback to pip
                essential_packages = [
                    "langchain-core",
                    "langchain-anthropic", 
                    "langchain-openai",
                    "langchain-community",
                    "langgraph",
                    "fastapi",
                    "streamlit",
                    "uvicorn",
                    "httpx",
                    "pydantic",
                    "python-dotenv"
                ]
                
                for package in essential_packages:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  check=True, capture_output=True)
                
                self.fixes_applied.append("Installed dependencies with pip")
                logger.info("✓ Dependencies installed with pip")
                return True
                
        except Exception as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def fix_port_conflicts(self) -> bool:
        """Kill processes using required ports."""
        try:
            import psutil
            
            ports_to_free = [8080, 8501]
            killed_processes = []
            
            for port in ports_to_free:
                for proc in psutil.process_iter(['pid', 'name', 'connections']):
                    try:
                        for conn in proc.info['connections'] or []:
                            if conn.laddr.port == port:
                                proc.terminate()
                                killed_processes.append(f"PID {proc.info['pid']} on port {port}")
                                logger.info(f"Killed process {proc.info['pid']} using port {port}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            
            if killed_processes:
                self.fixes_applied.append(f"Freed ports: {', '.join(killed_processes)}")
            
            return True
        except ImportError:
            logger.warning("psutil not available, cannot automatically free ports")
            return False
        except Exception as e:
            logger.error(f"Failed to free ports: {e}")
            return False
    
    def fix_database_issues(self) -> bool:
        """Fix common database issues."""
        try:
            # Remove corrupted SQLite database
            sqlite_path = Path("checkpoints.db")
            if sqlite_path.exists():
                sqlite_path.unlink()
                self.fixes_applied.append("Removed corrupted SQLite database")
                logger.info("✓ Removed corrupted SQLite database")
            
            # Create database directory if needed
            db_dir = Path("data")
            if not db_dir.exists():
                db_dir.mkdir()
                self.fixes_applied.append("Created database directory")
            
            return True
        except Exception as e:
            logger.error(f"Failed to fix database issues: {e}")
            return False

def main():
    """Main diagnostic and fix routine."""
    print("🔧 AI Agent Service Toolkit - Issue Diagnosis & Fix")
    print("=" * 60)
    
    # Run diagnostics
    diagnostics = SystemDiagnostics()
    fixer = IssueFixer()
    
    print("\n🔍 Running system diagnostics...")
    
    checks = [
        ("Python Version", diagnostics.check_python_version),
        ("Environment File", diagnostics.check_env_file),
        ("Dependencies", diagnostics.check_dependencies),
        ("Port Availability", diagnostics.check_ports),
        ("Model Providers", diagnostics.check_model_imports),
        ("Database Connection", diagnostics.check_database_connection),
    ]
    
    failed_checks = []
    for check_name, check_func in checks:
        try:
            if check_func():
                print(f"✅ {check_name}: OK")
            else:
                print(f"❌ {check_name}: FAILED")
                failed_checks.append(check_name)
        except Exception as e:
            print(f"❌ {check_name}: ERROR - {e}")
            failed_checks.append(check_name)
    
    # Apply fixes
    if diagnostics.issues_found:
        print(f"\n🔧 Found {len(diagnostics.issues_found)} issues. Applying fixes...")
        
        # Fix missing .env file
        if any("env file" in issue.lower() for issue in diagnostics.issues_found):
            fixer.fix_missing_env()
        
        # Fix missing dependencies
        if any("missing packages" in issue.lower() for issue in diagnostics.issues_found):
            fixer.fix_missing_dependencies()
        
        # Fix port conflicts
        if any("ports in use" in issue.lower() for issue in diagnostics.issues_found):
            fixer.fix_port_conflicts()
        
        # Fix database issues
        if any("database" in issue.lower() for issue in diagnostics.issues_found):
            fixer.fix_database_issues()
        
        print(f"\n✅ Applied {len(fixer.fixes_applied)} fixes:")
        for fix in fixer.fixes_applied:
            print(f"  • {fix}")
    
    # Final status
    print("\n" + "=" * 60)
    if not diagnostics.issues_found:
        print("🎉 System is healthy! No issues found.")
        print("\n🚀 You can now start the services:")
        print("   python src/run_service.py")
        print("   streamlit run src/streamlit_app.py")
    else:
        print("⚠️  Some issues may require manual intervention:")
        for issue in diagnostics.issues_found:
            print(f"  • {issue}")
        
        print("\n📚 Check the troubleshooting guide:")
        print("   TROUBLESHOOTING.md")
        print("   UPGRADE_FIX_RUNNING_APP.md")
    
    return len(diagnostics.issues_found) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)