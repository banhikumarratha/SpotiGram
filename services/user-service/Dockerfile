FROM python:3.11-slim

WORKDIR /app
COPY services/user-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY libs/ libs/
COPY services/user-service/ services/user-service/

ENV PYTHONPATH=/app
CMD ["uvicorn", "services.user-service.main:app", "--host", "0.0.0.0", "--port", "8000"]
