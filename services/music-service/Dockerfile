FROM python:3.11-slim

WORKDIR /app
COPY services/music-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY libs/ libs/
COPY services/music-service/ services/music-service/

ENV PYTHONPATH=/app
CMD ["uvicorn", "services.music-service.main:app", "--host", "0.0.0.0", "--port", "8002"]
