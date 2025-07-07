#!/bin/bash
# Quick dependency installer for macOS/Linux

echo "🚀 Installing AI Agent Service Toolkit Dependencies"
echo "=================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $python_version"

# Create .env if missing
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "USE_FAKE_MODEL=true" > .env
    echo "✅ Created .env file"
fi

# Install uv
echo "🔧 Installing uv package manager..."
python3 -m pip install uv

# Install dependencies
echo "📦 Installing project dependencies..."
if ! uv sync --frozen; then
    echo "⚠️  uv failed, using pip fallback..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install core packages
    pip install --upgrade pip
    pip install langchain-anthropic langchain-openai langchain-google-genai
    pip install langchain-groq langchain-community langchain-core
    pip install langgraph fastapi streamlit uvicorn httpx pydantic python-dotenv
    pip install duckduckgo-search numexpr pandas
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To start the service:"
echo "   1. source .venv/bin/activate"
echo "   2. python src/run_service.py"
echo ""
echo "🌐 To start the web app (in another terminal):"
echo "   1. source .venv/bin/activate" 
echo "   2. streamlit run src/streamlit_app.py"