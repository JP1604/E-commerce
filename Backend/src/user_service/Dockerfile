FROM python:3.11-slim

WORKDIR /app

RUN apt-get update -y && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Prefer mounted source over installed package for hot-reload
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

COPY ../../pyproject.toml ./pyproject.toml
COPY ./src/user_service ./src/user_service

RUN pip install --upgrade pip \
    && pip install .

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:8001/ || exit 1

CMD ["uvicorn", "user_service.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

