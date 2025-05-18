#!/bin/bash

# Source directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# Validate environment
./scripts/validate_environment.sh
if [ $? -ne 0 ]; then
  echo "Environment validation failed"
  exit 1
fi

# Function to wait for service health
wait_for_healthy() {
  local service=$1
  local timeout=$2
  local count=0
  echo "Waiting for $service to be healthy..."
  while [ $count -lt $timeout ]; do
    if docker compose ps $service | grep -q "healthy"; then
      echo "$service is healthy"
      return 0
    fi
    sleep 1
    count=$((count + 1))
  done
  echo "$service failed to become healthy within $timeout seconds"
  return 1
}

# Start services
echo "Starting AutoDev Commander services..."
docker compose -f docker/compose/base.yml -f docker/compose/dev.yml up -d

# Wait for core services
wait_for_healthy "redis" 30
wait_for_healthy "qdrant" 60
wait_for_healthy "ollama" 60

echo "AutoDev Commander is ready!"
docker compose ps
