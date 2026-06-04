FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file
COPY services/api-template/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared utilities
COPY libs/ libs/

# Copy the service code
COPY services/api-template/ services/api-template/

# Set Python path to allow imports from libs
ENV PYTHONPATH=/app

# Run the application
CMD ["uvicorn", "services.api-template.main:app", "--host", "0.0.0.0", "--port", "8000"]
