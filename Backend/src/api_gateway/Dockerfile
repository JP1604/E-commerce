FROM python:3.11-slim

WORKDIR /app

RUN apt-get update -y && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

COPY ../../pyproject.toml ./pyproject.toml
COPY ./src/api_gateway ./src/api_gateway

RUN pip install --upgrade pip \
    && pip install .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8080/ || exit 1

CMD ["uvicorn", "api_gateway.main:app", "--host", "0.0.0.0", "--port", "8080"]


