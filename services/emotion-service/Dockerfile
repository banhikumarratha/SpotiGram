FROM python:3.11-slim

WORKDIR /app
COPY services/emotion-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Download textblob corporas
RUN python -m textblob.download_corpora

COPY libs/ libs/
COPY services/emotion-service/ services/emotion-service/

ENV PYTHONPATH=/app
CMD ["uvicorn", "services.emotion-service.main:app", "--host", "0.0.0.0", "--port", "8005"]
