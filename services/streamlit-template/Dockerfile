FROM python:3.12-slim

WORKDIR /app

# Copy shared package
COPY packages/shared /packages/shared

# Copy service files
COPY services/streamlit-template/pyproject.toml .
COPY services/streamlit-template/src ./src

# Install dependencies
RUN pip install --no-cache-dir .

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
