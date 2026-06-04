FROM python:3.11-slim

WORKDIR /app
COPY services/ai-assistant-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY libs/ libs/
COPY services/ai-assistant-service/ services/ai-assistant-service/

ENV PYTHONPATH=/app
CMD ["uvicorn", "services.ai-assistant-service.main:app", "--host", "0.0.0.0", "--port", "8003"]
