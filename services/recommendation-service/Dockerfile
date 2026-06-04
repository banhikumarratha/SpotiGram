FROM python:3.11-slim

WORKDIR /app
COPY services/recommendation-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY libs/ libs/
COPY services/recommendation-service/ services/recommendation-service/

ENV PYTHONPATH=/app
CMD ["uvicorn", "services.recommendation-service.main:app", "--host", "0.0.0.0", "--port", "8007"]
