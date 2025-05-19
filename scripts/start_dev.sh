#!/bin/bash
# Path: ~/AutoDev-Commander/scripts/start_dev.sh

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Load environment variables
set -a
source "${PROJECT_ROOT}/.env"
set +a

echo "Starting AutoDev Commander Development Environment..."
echo "Project root: ${PROJECT_ROOT}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# Start core services
echo "Starting core services..."
docker compose -f "${PROJECT_ROOT}/docker/compose/base.yml" up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
for service in ollama qdrant redis; do
    echo "Waiting for $service..."
    while ! docker compose -f "${PROJECT_ROOT}/docker/compose/base.yml" ps $service | grep -q "healthy"; do
        sleep 5
    done
    echo "$service is ready!"
done

# Start FastAPI application in development mode
echo "Starting FastAPI application..."
cd "${PROJECT_ROOT}/src"
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
