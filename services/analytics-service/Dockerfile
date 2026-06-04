FROM python:3.11-slim
WORKDIR /app
COPY packages /packages
COPY services/analytics-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/analytics-service .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
