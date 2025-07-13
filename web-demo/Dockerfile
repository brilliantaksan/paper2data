FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Paper2Data
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    poppler-utils \
    libfontconfig1 \
    libxext6 \
    libxrender1 \
    libfreetype6-dev \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (includes paper2data_local/)
COPY . .

# Set Python path to include local Paper2Data
ENV PYTHONPATH="/app:/app/paper2data_local:${PYTHONPATH}"

# Create temp directory
RUN mkdir -p /tmp/paper2data_web

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Run the application using environment PORT variable
CMD ["sh", "-c", "uvicorn main_full_working:app --host 0.0.0.0 --port ${PORT:-8000}"]
