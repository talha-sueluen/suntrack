FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY backend/ backend/
COPY frontend/ frontend/

RUN pip install requests python-dotenv streamlit pandas plotly

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "frontend/dashboard.py", "--server.address=0.0.0.0"]