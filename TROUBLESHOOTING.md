# 🔧 Troubleshooting Guide - Internal Server Error Fix

If you're getting an "Internal server error", follow these steps to diagnose and fix the issue.

## 🚨 Quick Fix Steps

### Step 1: Run the Fix Script
```bash
python fix_setup.py
```

This script will automatically:
- Check Python version compatibility
- Create/fix your .env file
- Install missing dependencies
- Check for port conflicts
- Create startup scripts

### Step 2: Manual Fixes

If the script doesn't resolve the issue, try these manual steps:

#### A. Check Python Version
```bash
python --version
```
**Required:** Python 3.11 or higher

#### B. Fix Environment File
1. Make sure `.env` file exists:
   ```bash
   cp .env.example .env
   ```

2. Add at least one API key OR enable fake model:
   ```bash
   # Edit .env file and add:
   USE_FAKE_MODEL=true
   
   # OR add a real API key:
   OPENAI_API_KEY=your_key_here
   ```

#### C. Install Dependencies
```bash
# Method 1: Using uv (recommended)
pip install uv
uv sync --frozen

# Method 2: Using pip (fallback)
pip install .
```

#### D. Check for Port Conflicts
```bash
# Check if ports 8080 and 8501 are free
netstat -an | grep :8080
netstat -an | grep :8501
```

## 🐛 Common Error Messages & Solutions

### Error: "At least one LLM API key must be provided"
**Solution:**
```bash
# Edit .env file and add:
USE_FAKE_MODEL=true
```

### Error: "ModuleNotFoundError"
**Solution:**
```bash
# Reinstall dependencies
pip install uv
uv sync --frozen --no-cache
```

### Error: "Port already in use"
**Solution:**
```bash
# Option 1: Kill processes using the ports
# Windows:
netstat -ano | findstr :8080
taskkill /PID <PID_NUMBER> /F

# macOS/Linux:
lsof -ti:8080 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Option 2: Change ports in .env
PORT=8081
```

### Error: "Permission denied" (macOS/Linux)
**Solution:**
```bash
chmod +x start_unix.sh
```

## 🔄 Step-by-Step Restart Process

### For Docker Users:
```bash
# Stop all containers
docker compose down

# Remove volumes (if needed)
docker compose down -v

# Rebuild and start
docker compose up --build
```

### For Local Python Users:
```bash
# 1. Stop all running processes (Ctrl+C)

# 2. Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# 3. Start FastAPI service
python src/run_service.py

# 4. In new terminal, start Streamlit
source .venv/bin/activate  # macOS/Linux
streamlit run src/streamlit_app.py
```

## 🧪 Test Your Setup

### 1. Test FastAPI Service
```bash
curl http://localhost:8080/health
```
**Expected response:** `{"status": "ok"}`

### 2. Test Streamlit App
Open browser: http://localhost:8501

### 3. Test Agent Response
In Streamlit app, try asking: "Hello, how are you?"

## 📋 Environment Validation Checklist

- [ ] Python 3.11+ installed
- [ ] `.env` file exists with API key OR `USE_FAKE_MODEL=true`
- [ ] Dependencies installed (`uv sync --frozen` or `pip install .`)
- [ ] Ports 8080 and 8501 are available
- [ ] Virtual environment activated
- [ ] No firewall blocking localhost connections

## 🆘 Still Having Issues?

### Collect Debug Information:
```bash
# System info
python --version
pip list | grep -E "(langchain|streamlit|fastapi)"

# Check processes
ps aux | grep python  # macOS/Linux
tasklist | findstr python  # Windows

# Check logs
# Look for error messages in terminal output
```

### Get Help:
1. **GitHub Issues:** https://github.com/JoshuaC215/agent-service-toolkit/issues
2. **Include in your issue:**
   - Operating system
   - Python version
   - Error message (full traceback)
   - Steps you've already tried

## 🎯 Alternative Quick Start (Minimal Setup)

If you just want to test the project quickly:

```bash
# 1. Clone and enter directory
git clone https://github.com/JoshuaC215/agent-service-toolkit.git
cd agent-service-toolkit

# 2. Create minimal .env
echo "USE_FAKE_MODEL=true" > .env

# 3. Install and run
pip install uv
uv sync --frozen
python fix_setup.py

# 4. Use startup script
./start_unix.sh    # macOS/Linux
# OR
start_windows.bat  # Windows
```

This will get you running with a fake model for testing purposes.