FROM python:3.11-slim

WORKDIR /app

# Install build deps for psycopg/asyncpg if needed
RUN apt-get update -y && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./pyproject.toml
COPY ./src ./src
COPY ./main.py ./main.py

RUN pip install --upgrade pip \
    && pip install .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]