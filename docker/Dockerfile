# Path: ~/AutoDev-Commander/docker/Dockerfile
# Builder stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies and Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    /root/.local/bin/poetry --version

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only dependency files first
COPY pyproject.toml poetry.lock* ./

# Generate requirements file - Updated command
RUN poetry install --no-root && \
    poetry run pip freeze > requirements.txt

# Development stage
FROM python:3.11-slim as dev

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    debugpy \
    pytest \
    black \
    ruff \
    mypy

# Copy project files
COPY . .

# Development command
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
