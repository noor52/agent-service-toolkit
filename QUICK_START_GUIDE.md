# 🚀 Quick Start Guide - AI Agent Service Toolkit

This guide will get you up and running in **5 minutes** with the optimal configuration for coding and development.

## 📋 Prerequisites

- **Python 3.11+** (Check: `python --version`)
- **Git** (for cloning the repository)
- **Terminal/Command Prompt** access

## ⚡ Super Quick Start (Recommended)

### 1. Clone and Enter Directory
```bash
git clone https://github.com/JoshuaC215/agent-service-toolkit.git
cd agent-service-toolkit
```

### 2. Run the Final Fix Script
```bash
python FINAL_FIX.py
```

This script will automatically:
- ✅ Check your Python version
- ✅ Create optimized `.env` configuration
- ✅ Install all dependencies
- ✅ Free up required ports
- ✅ Test all functionality
- ✅ Create startup scripts

### 3. Start the Services

**Option A - Use Startup Scripts (Easiest):**
```bash
# Windows
start_services.bat

# macOS/Linux
./start_services.sh
```

**Option B - Manual Start:**
```bash
# Terminal 1: Start FastAPI service
python src/run_service.py

# Terminal 2: Start Streamlit app
streamlit run src/streamlit_app.py
```

### 4. Open Your Browser
- **Streamlit App**: http://localhost:8501
- **API Documentation**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/health

## 🎯 Default Configuration (Perfect for Coding)

The `FINAL_FIX.py` script sets up an optimal configuration:

### 🤖 **Default Model: FAKE MODEL**
- **Why**: Instant responses, no API costs, perfect for testing
- **Usage**: Works immediately without any API keys
- **Responses**: Consistent test responses for development

### 🗄️ **Database: SQLite**
- **Why**: Zero configuration, file-based, perfect for development
- **Location**: `checkpoints.db` (created automatically)
- **Features**: Conversation history, thread management

### 🔐 **Authentication: Disabled**
- **Why**: Easier development and testing
- **Security**: Enable in production by setting `AUTH_SECRET`

### 🌐 **Development Mode**
- **Auto-reload**: Code changes trigger automatic restarts
- **Debug info**: Enhanced error messages and logging
- **Hot reload**: Streamlit auto-refreshes on changes

## 🧪 Test Your Setup

### 1. Basic Functionality Test
Open http://localhost:8501 and try:
```
Hello, how are you?
```
**Expected**: Fake model response

### 2. Agent Selection Test
In the Streamlit sidebar:
- Change agent to "research-assistant"
- Ask: "What is 2 + 2?"
**Expected**: Calculator tool usage

### 3. API Test
```bash
curl http://localhost:8080/health
```
**Expected**: `{"status": "ok"}`

## 🔧 Available Agents (All Ready to Use)

| Agent | Description | Best For |
|-------|-------------|----------|
| **chatbot** | Simple conversational AI | Basic testing |
| **research-assistant** | Web search + calculator | Development demos |
| **rag-assistant** | Document Q&A | RAG development |
| **interrupt-agent** | Interactive prompts | Human-in-loop testing |
| **command-agent** | Flow control demo | Graph logic testing |
| **bg-task-agent** | Background tasks | Async development |

## 🚀 Production Upgrade Path

When ready for production, simply:

### 1. Add Real API Keys to `.env`
```bash
# Uncomment and add your keys
OPENAI_API_KEY=sk-your-key-here
# or
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 2. Update Default Model
```bash
# In .env file, change:
USE_FAKE_MODEL=false
DEFAULT_MODEL=gpt-4o-mini
```

### 3. Enable Authentication
```bash
# In .env file, add:
AUTH_SECRET=your-secret-key-here
```

### 4. Switch to PostgreSQL (Optional)
```bash
# In .env file:
DATABASE_TYPE=postgres
POSTGRES_HOST=your-host
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
POSTGRES_DB=your-database
```

## 🔍 Troubleshooting

### Issue: "Module not found" errors
**Solution**: Run `python FINAL_FIX.py` again

### Issue: Ports already in use
**Solution**: The fix script automatically handles this

### Issue: Streamlit won't start
**Solution**: 
```bash
# Check if service is running
curl http://localhost:8080/health

# If not, restart FastAPI first
python src/run_service.py
```

### Issue: Fake model not working
**Solution**: Check `.env` file contains:
```bash
USE_FAKE_MODEL=true
DEFAULT_MODEL=fake
```

## 📚 Next Steps

### For Development:
1. **Explore Agents**: Try different agents in the sidebar
2. **Modify Code**: Edit agents in `src/agents/`
3. **Add Tools**: Create custom tools in `src/agents/tools.py`
4. **Test Streaming**: Enable/disable streaming in settings

### For Production:
1. **Add API Keys**: Get keys from OpenAI, Anthropic, etc.
2. **Setup Database**: Configure PostgreSQL for scalability
3. **Enable Monitoring**: Add LangSmith or Langfuse tracing
4. **Deploy**: Use Docker compose for production deployment

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ Streamlit app loads at http://localhost:8501
- ✅ You can chat with the fake model
- ✅ Agent switching works in sidebar
- ✅ API health check returns OK
- ✅ No error messages in terminals

## 🆘 Need Help?

- **GitHub Issues**: https://github.com/JoshuaC215/agent-service-toolkit/issues
- **Documentation**: Check `README.md` and `TROUBLESHOOTING.md`
- **Discord/Community**: Join the discussions

---

**🎯 Goal**: Get you coding with AI agents in under 5 minutes!  
**🚀 Result**: Fully functional AI agent service ready for development!