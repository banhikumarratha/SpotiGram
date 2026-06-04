FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file
COPY services/ui-template/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared utilities
COPY libs/ libs/

# Copy the service code
COPY services/ui-template/ services/ui-template/

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "services/ui-template/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
