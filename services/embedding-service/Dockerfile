FROM python:3.11-slim

WORKDIR /app
COPY services/embedding-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the model to cache it in the image layer
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY libs/ libs/
COPY services/embedding-service/ services/embedding-service/

ENV PYTHONPATH=/app
CMD ["uvicorn", "services.embedding-service.main:app", "--host", "0.0.0.0", "--port", "8006"]
