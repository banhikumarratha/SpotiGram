FROM python:3.12-slim

WORKDIR /app

# Copy shared package
COPY packages/shared /packages/shared

# Copy service files
COPY services/fastapi-template/pyproject.toml .
COPY services/fastapi-template/src ./src

# Install dependencies
RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
