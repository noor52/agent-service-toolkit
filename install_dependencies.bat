@echo off
REM Quick dependency installer for Windows

echo 🚀 Installing AI Agent Service Toolkit Dependencies
echo ==================================================

REM Check if .env exists
if not exist ".env" (
    echo 📝 Creating .env file...
    echo USE_FAKE_MODEL=true > .env
    echo ✅ Created .env file
)

REM Install uv
echo 🔧 Installing uv package manager...
python -m pip install uv

REM Install dependencies
echo 📦 Installing project dependencies...
uv sync --frozen
if errorlevel 1 (
    echo ⚠️  uv failed, using pip fallback...
    
    REM Create virtual environment if it doesn't exist
    if not exist ".venv" (
        python -m venv .venv
    )
    
    REM Activate virtual environment
    call .venv\Scripts\activate.bat
    
    REM Install core packages
    pip install --upgrade pip
    pip install langchain-anthropic langchain-openai langchain-google-genai
    pip install langchain-groq langchain-community langchain-core
    pip install langgraph fastapi streamlit uvicorn httpx pydantic python-dotenv
    pip install duckduckgo-search numexpr pandas
)

echo.
echo ✅ Installation complete!
echo.
echo 🚀 To start the service:
echo    1. .venv\Scripts\activate.bat
echo    2. python src\run_service.py
echo.
echo 🌐 To start the web app (in another terminal):
echo    1. .venv\Scripts\activate.bat
echo    2. streamlit run src\streamlit_app.py
echo.
pause