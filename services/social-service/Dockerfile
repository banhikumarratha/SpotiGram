FROM python:3.11-slim

WORKDIR /app
COPY services/social-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY libs/ libs/
COPY services/social-service/ services/social-service/

ENV PYTHONPATH=/app
CMD ["uvicorn", "services.social-service.main:app", "--host", "0.0.0.0", "--port", "8001"]
