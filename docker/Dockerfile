FROM python:3.10-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose both ports
EXPOSE 8000 8501

ENV PYTHONPATH=/app

# Use a startup script that waits for FastAPI before starting Streamlit
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & sleep 5 && streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true"]