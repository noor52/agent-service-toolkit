#!/bin/bash
echo "Starting AI Agent Service Toolkit..."
echo

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing/updating dependencies..."
pip install uv
uv sync --frozen

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
trap "kill $SERVICE_PID $APP_PID 2>/dev/null; exit" INT
wait