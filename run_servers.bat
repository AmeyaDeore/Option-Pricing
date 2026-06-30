@echo off
echo Starting FastAPI Backend...
start cmd /k "cd iv-surface-project && .\venv\Scripts\activate && uvicorn main:app --reload"

echo Starting Streamlit Frontend...
start cmd /k "cd iv-surface-project && .\venv\Scripts\activate && streamlit run app.py"

echo Both servers are starting!
