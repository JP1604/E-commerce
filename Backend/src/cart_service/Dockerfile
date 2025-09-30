FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Expose port
EXPOSE 8003

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PORT=8003

# Run the application
CMD ["uvicorn", "cart_service.main:app", "--host", "0.0.0.0", "--port", "8003"]
