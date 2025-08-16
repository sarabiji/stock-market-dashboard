
# Simple Dockerfile for the API + static frontend
FROM python:3.11-slim

WORKDIR /app

# System deps (optional: tzdata for logs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend

ENV PORT=8000

EXPOSE 8000

CMD ["python", "backend/main.py"]
