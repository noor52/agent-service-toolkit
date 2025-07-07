# 🚀 AI Agent Service Toolkit - Easy Setup Guide

This guide will help you set up and run the AI Agent Service Toolkit on your local machine step by step.

## 📋 Prerequisites

Before starting, make sure you have the following installed on your PC:

1. **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
2. **Git** - [Download Git](https://git-scm.com/downloads)
3. **Docker & Docker Compose** (Optional but recommended) - [Download Docker](https://www.docker.com/products/docker-desktop/)

## 🔧 Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
git clone https://github.com/JoshuaC215/agent-service-toolkit.git
cd agent-service-toolkit
```

## 🔑 Step 2: Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add at least one API key:
   ```bash
   # Choose ONE or more of these API keys:
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

   **Where to get API keys:**
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google AI: https://ai.google.dev/
   - Groq: https://console.groq.com/

## 🚀 Step 3: Choose Your Setup Method

### Option A: Docker Setup (Recommended - Easier)

1. **Install Docker Desktop** if you haven't already
2. **Start the services:**
   ```bash
   docker compose watch
   ```
3. **Wait for services to start** (this may take a few minutes on first run)
4. **Access the application:**
   - Streamlit App: http://localhost:8501
   - API Documentation: http://localhost:8080/redoc

### Option B: Local Python Setup

1. **Install uv (recommended package manager):**
   ```bash
   pip install uv
   ```

2. **Install dependencies:**
   ```bash
   uv sync --frozen
   ```

3. **Activate virtual environment:**
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Start the FastAPI service** (in first terminal):
   ```bash
   python src/run_service.py
   ```

5. **Start the Streamlit app** (in second terminal):
   ```bash
   # Activate virtual environment again
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   streamlit run src/streamlit_app.py
   ```

6. **Access the application:**
   - Streamlit App: http://localhost:8501
   - API Documentation: http://localhost:8080/redoc

## 🧪 Step 4: Test Your Setup

1. **Open the Streamlit app** at http://localhost:8501
2. **Try asking a question** like "Tell me a joke" or "What's the weather like?"
3. **Verify the response** - you should see the AI agent responding

## 🛠️ Step 5: Customize Your Agent (Optional)

### Available Agents:
- **research-assistant**: Web search + calculator
- **chatbot**: Simple conversational AI
- **rag-assistant**: Document-based Q&A (requires setup)
- **interrupt-agent**: Interactive agent with user prompts

### Switch Agents:
1. In the Streamlit app, use the sidebar settings
2. Select different agents from the dropdown
3. Try different models if you have multiple API keys

## 🔍 Troubleshooting

### Common Issues:

1. **"No API key provided" error:**
   - Make sure you've added at least one API key to your `.env` file
   - Restart the services after adding the key

2. **Port already in use:**
   - Change ports in `.env` file:
     ```
     PORT=8081  # for FastAPI service
     ```
   - For Streamlit, use: `streamlit run src/streamlit_app.py --server.port 8502`

3. **Docker issues:**
   - Make sure Docker Desktop is running
   - Try: `docker compose down` then `docker compose up --build`

4. **Python dependency issues:**
   - Try: `uv sync --frozen --no-cache`
   - Make sure you're using Python 3.11+

### Getting Help:
- Check the [GitHub Issues](https://github.com/JoshuaC215/agent-service-toolkit/issues)
- Read the full [README.md](README.md) for detailed information

## 🎯 Next Steps

Once you have the basic setup working:

1. **Explore different agents** in the sidebar
2. **Try the RAG assistant** by following [docs/RAG_Assistant.md](docs/RAG_Assistant.md)
3. **Set up additional providers** like Ollama or VertexAI
4. **Build your own agent** by copying existing agents in `src/agents/`

## 📚 Additional Resources

- **Architecture Overview**: Check the architecture diagram in the Streamlit app
- **API Documentation**: Visit http://localhost:8080/redoc when running
- **Video Walkthrough**: https://www.youtube.com/watch?v=pdYVHw_YCNY
- **Source Code**: https://github.com/JoshuaC215/agent-service-toolkit

---

🎉 **Congratulations!** You now have a fully functional AI Agent Service running on your machine!