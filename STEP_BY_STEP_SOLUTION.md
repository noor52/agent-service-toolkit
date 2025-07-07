# 📋 Step-by-Step Solution Guide

This comprehensive guide provides detailed instructions for setting up, running, and troubleshooting the AI Agent Service Toolkit.

## 🎯 Overview

This guide covers:
1. **Complete Setup** - From zero to running application
2. **Default Configuration** - Optimal settings for development
3. **Troubleshooting** - Solutions for common issues
4. **Production Deployment** - Scaling for real-world use

---

## 🚀 PHASE 1: Initial Setup

### Step 1: System Requirements Check

#### 1.1 Verify Python Version
```bash
python --version
# Required: Python 3.11 or higher
```

**If Python is too old:**
- **Windows**: Download from https://python.org/downloads/
- **macOS**: `brew install python@3.11` or download from python.org
- **Linux**: `sudo apt update && sudo apt install python3.11`

#### 1.2 Verify Git Installation
```bash
git --version
# Should show git version
```

**If Git is missing:**
- **Windows**: Download from https://git-scm.com/
- **macOS**: `xcode-select --install`
- **Linux**: `sudo apt install git`

### Step 2: Project Setup

#### 2.1 Clone Repository
```bash
# Clone the project
git clone https://github.com/JoshuaC215/agent-service-toolkit.git

# Enter project directory
cd agent-service-toolkit

# Verify project structure
ls -la
# Should see: src/, docker/, pyproject.toml, README.md, etc.
```

#### 2.2 Run Automated Fix
```bash
# Run the comprehensive fix script
python FINAL_FIX.py
```

**What this script does:**
- ✅ Checks Python version compatibility
- ✅ Creates optimized `.env` configuration
- ✅ Installs UV package manager
- ✅ Installs all required dependencies
- ✅ Frees up required ports (8080, 8501)
- ✅ Tests all critical imports
- ✅ Validates core functionality
- ✅ Creates convenient startup scripts

---

## 🔧 PHASE 2: Configuration Details

### Step 3: Understanding the Default Configuration

#### 3.1 Environment File (`.env`)
The script creates an optimized `.env` file:

```bash
# View the configuration
cat .env
```

**Key settings:**
```bash
# Default model for development
USE_FAKE_MODEL=true
DEFAULT_MODEL=fake

# Server configuration
HOST=0.0.0.0
PORT=8080

# Database (SQLite for development)
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=checkpoints.db

# Development mode
MODE=dev
```

#### 3.2 Why These Defaults?

**FAKE MODEL Benefits:**
- 🆓 **Zero cost** - No API charges
- ⚡ **Instant responses** - No network latency
- 🔄 **Consistent output** - Predictable for testing
- 🚫 **No rate limits** - Unlimited requests
- 📱 **Offline capable** - Works without internet

**SQLite Database Benefits:**
- 📁 **File-based** - No server setup required
- 🔧 **Zero configuration** - Works out of the box
- 💾 **Persistent** - Saves conversation history
- 🔄 **Portable** - Easy to backup/restore

### Step 4: Dependency Verification

#### 4.1 Check Installed Packages
```bash
# If using UV (recommended)
uv tree

# Or with pip
pip list | grep -E "(langchain|langgraph|fastapi|streamlit)"
```

#### 4.2 Test Critical Imports
```bash
python -c "
import langchain_core
import langgraph
import fastapi
import streamlit
print('✅ All critical packages imported successfully')
"
```

---

## 🏃 PHASE 3: Running the Application

### Step 5: Start Services

#### 5.1 Option A: Use Startup Scripts (Recommended)

**Windows:**
```cmd
start_services.bat
```

**macOS/Linux:**
```bash
chmod +x start_services.sh
./start_services.sh
```

#### 5.2 Option B: Manual Start

**Terminal 1 - FastAPI Service:**
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Start FastAPI service
python src/run_service.py
```

**Expected output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

**Terminal 2 - Streamlit App:**
```bash
# Activate virtual environment (if using one)
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Start Streamlit app
streamlit run src/streamlit_app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

### Step 6: Verify Installation

#### 6.1 Health Check
```bash
# Test FastAPI service
curl http://localhost:8080/health
# Expected: {"status": "ok"}

# Test service info
curl http://localhost:8080/info
# Expected: JSON with agents and models list
```

#### 6.2 Web Interface Test
1. **Open browser**: http://localhost:8501
2. **Expected**: Streamlit chat interface loads
3. **Test message**: Type "Hello, how are you?"
4. **Expected**: Fake model responds with test message

#### 6.3 Agent Switching Test
1. **In Streamlit sidebar**: Click "Settings"
2. **Change agent**: Select "research-assistant"
3. **Test calculation**: Ask "What is 2 + 2?"
4. **Expected**: Calculator tool is used, shows result "4"

---

## 🔍 PHASE 4: Troubleshooting Common Issues

### Issue 1: "Module not found" Errors

#### Symptoms:
```
ModuleNotFoundError: No module named 'langchain_anthropic'
```

#### Solutions:

**Solution A: Re-run Fix Script**
```bash
python FINAL_FIX.py
```

**Solution B: Manual Dependency Install**
```bash
# Install UV if not available
pip install uv

# Install dependencies
uv sync --frozen

# If UV fails, use pip
pip install langchain-anthropic langchain-openai langgraph fastapi streamlit
```

**Solution C: Virtual Environment Reset**
```bash
# Remove existing environment
rm -rf .venv

# Create new environment
python -m venv .venv

# Activate and install
source .venv/bin/activate  # macOS/Linux
pip install uv
uv sync
```

### Issue 2: Port Already in Use

#### Symptoms:
```
OSError: [Errno 48] Address already in use
```

#### Solutions:

**Solution A: Automatic Port Cleanup**
```bash
python FINAL_FIX.py
# Script automatically frees ports
```

**Solution B: Manual Port Cleanup**

**Find processes using ports:**
```bash
# macOS/Linux
lsof -ti:8080 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID_NUMBER> /F
```

**Solution C: Use Different Ports**
```bash
# Edit .env file
PORT=8081

# Start Streamlit on different port
streamlit run src/streamlit_app.py --server.port 8502
```

### Issue 3: Database Connection Errors

#### Symptoms:
```
sqlite3.OperationalError: database is locked
```

#### Solutions:

**Solution A: Reset Database**
```bash
# Remove corrupted database
rm checkpoints.db

# Restart services (database will be recreated)
python src/run_service.py
```

**Solution B: Check File Permissions**
```bash
# Ensure write permissions
chmod 666 checkpoints.db
chmod 777 .  # For directory
```

### Issue 4: Streamlit Won't Load

#### Symptoms:
- Browser shows "This site can't be reached"
- Streamlit starts but shows errors

#### Solutions:

**Solution A: Check FastAPI Service**
```bash
# Ensure FastAPI is running first
curl http://localhost:8080/health

# If not running, start it
python src/run_service.py
```

**Solution B: Clear Streamlit Cache**
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart Streamlit
streamlit run src/streamlit_app.py
```

**Solution C: Check Environment Variables**
```bash
# Verify .env file exists and has correct settings
cat .env | grep -E "(USE_FAKE_MODEL|DEFAULT_MODEL)"
```

### Issue 5: Fake Model Not Working

#### Symptoms:
- Error: "No API key provided"
- Model selection shows no fake model

#### Solutions:

**Solution A: Verify .env Configuration**
```bash
# Check .env file contains:
grep "USE_FAKE_MODEL=true" .env
grep "DEFAULT_MODEL=fake" .env

# If missing, add them:
echo "USE_FAKE_MODEL=true" >> .env
echo "DEFAULT_MODEL=fake" >> .env
```

**Solution B: Restart Services**
```bash
# Stop all services (Ctrl+C)
# Then restart both:
python src/run_service.py
streamlit run src/streamlit_app.py
```

---

## 🚀 PHASE 5: Production Transition

### Step 7: Add Real API Keys

#### 7.1 Get API Keys

**OpenAI (Recommended):**
1. Visit: https://platform.openai.com/api-keys
2. Create account and add payment method
3. Generate API key (starts with `sk-`)

**Anthropic (Alternative):**
1. Visit: https://console.anthropic.com/
2. Create account and add payment method
3. Generate API key (starts with `sk-ant-`)

#### 7.2 Update Configuration
```bash
# Edit .env file
nano .env  # or your preferred editor

# Add your API key:
OPENAI_API_KEY=sk-your-actual-key-here

# Switch to real model:
USE_FAKE_MODEL=false
DEFAULT_MODEL=gpt-4o-mini
```

#### 7.3 Test Real Model
```bash
# Restart services
# Stop current services (Ctrl+C)
python src/run_service.py
streamlit run src/streamlit_app.py

# Test in browser
# Ask: "What's the weather like today?"
# Should get real AI response
```

### Step 8: Production Database Setup

#### 8.1 PostgreSQL Setup (Recommended for Production)

**Using Docker:**
```bash
# Start PostgreSQL container
docker run -d \
  --name postgres \
  -e POSTGRES_USER=agent_user \
  -e POSTGRES_PASSWORD=secure_password \
  -e POSTGRES_DB=agent_service \
  -p 5432:5432 \
  postgres:16

# Update .env file:
DATABASE_TYPE=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=agent_service
```

#### 8.2 Enable Authentication
```bash
# Add to .env file:
AUTH_SECRET=your-secure-secret-key-here

# Test with authentication:
curl -H "Authorization: Bearer your-secure-secret-key-here" \
  http://localhost:8080/health
```

### Step 9: Monitoring Setup

#### 9.1 Enable LangSmith Tracing
```bash
# Get API key from: https://smith.langchain.com/
# Add to .env:
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=agent-service-production
```

#### 9.2 Performance Monitoring
```bash
# Add performance logging
# Monitor response times in LangSmith dashboard
# Set up alerts for errors and slow responses
```

---

## 📊 PHASE 6: Validation & Testing

### Step 10: Comprehensive Testing

#### 10.1 Functional Tests
```bash
# Run test suite
python -m pytest tests/ -v

# Test specific components
python -m pytest tests/service/ -v
python -m pytest tests/client/ -v
```

#### 10.2 Load Testing
```bash
# Install load testing tools
pip install locust

# Create load test script
cat > load_test.py << EOF
from locust import HttpUser, task, between

class AgentUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_invoke(self):
        self.client.post("/invoke", json={"message": "Hello"})
EOF

# Run load test
locust -f load_test.py --host=http://localhost:8080
```

#### 10.3 Integration Tests
```bash
# Test all agents
agents=("chatbot" "research-assistant" "rag-assistant" "interrupt-agent")

for agent in "${agents[@]}"; do
    echo "Testing $agent..."
    curl -X POST http://localhost:8080/$agent/invoke \
      -H "Content-Type: application/json" \
      -d '{"message": "Hello from '$agent'"}'
done
```

---

## 🎯 Success Checklist

### ✅ Development Setup Complete When:
- [ ] Python 3.11+ installed and verified
- [ ] Project cloned and `FINAL_FIX.py` run successfully
- [ ] `.env` file created with `USE_FAKE_MODEL=true`
- [ ] All dependencies installed without errors
- [ ] FastAPI service starts on http://localhost:8080
- [ ] Streamlit app loads on http://localhost:8501
- [ ] Health check returns `{"status": "ok"}`
- [ ] Fake model responds to chat messages
- [ ] Agent switching works in sidebar
- [ ] Calculator tool works with research-assistant

### ✅ Production Ready When:
- [ ] Real API keys added and tested
- [ ] PostgreSQL database configured
- [ ] Authentication enabled and tested
- [ ] Monitoring/tracing configured
- [ ] Load testing completed
- [ ] All tests pass
- [ ] Error handling verified
- [ ] Backup procedures established

---

## 🆘 Getting Help

### Self-Help Resources:
1. **Re-run Fix Script**: `python FINAL_FIX.py`
2. **Check Logs**: Look for error messages in terminal output
3. **Verify Configuration**: Ensure `.env` file is correct
4. **Test Components**: Use curl commands to test API endpoints

### Community Support:
- **GitHub Issues**: https://github.com/JoshuaC215/agent-service-toolkit/issues
- **Documentation**: README.md, TROUBLESHOOTING.md
- **Examples**: Check `tests/` directory for usage examples

### When Reporting Issues:
Include:
- Operating system and Python version
- Complete error message/traceback
- Contents of `.env` file (remove API keys)
- Steps you've already tried
- Output of `python FINAL_FIX.py`

---

**🎉 Congratulations!** You now have a fully functional AI Agent Service Toolkit ready for development and production use!