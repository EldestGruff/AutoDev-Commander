#!/bin/bash

# Check if running as root
if [ "$EUID" -eq 0 ]; then
  echo "Please run without sudo"
  exit 1
fi

# Check for required commands
for cmd in docker docker-compose curl git; do
  if ! command -v $cmd &> /dev/null; then
    echo "Error: $cmd is required but not installed."
    exit 1
  fi
done

# Check if NVIDIA runtime is available
if ! docker info | grep -q "Runtimes.*nvidia"; then
  echo "Warning: NVIDIA runtime not found. GPU support may not be available."
fi

# Validate storage paths
for path in \
  /eniac/autodev/models/ollama \
  /eniac/autodev/qdrant_live/storage \
  /eniac/autodev/qdrant_live/snapshots \
  /eniac/autodev/redis \
  /eniac/autodev/n8n \
  /eniac/autodev/artifacts; do
  
  if [ ! -d "$path" ]; then
    echo "Creating directory: $path"
    sudo mkdir -p "$path"
    sudo chown -R $(id -u):$(id -g) "$path"
  fi
done

echo "Environment validation complete"
