FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src src
COPY main.py .

RUN pip install --upgrade pip \
    && pip install .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/ || exit 1
# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]