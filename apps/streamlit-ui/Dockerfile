FROM python:3.11-slim
WORKDIR /app
COPY packages /packages
COPY apps/streamlit-ui/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY apps/streamlit-ui .
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
