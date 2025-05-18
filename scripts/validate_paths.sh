#!/bin/bash

# Load environment variables
set -a
source ../.env
set +a

# Check required paths
required_paths=(
    "$STORAGE_BASE"
    "$MODELS_PATH"
    "$QDRANT_PATH"
    "$REDIS_PATH"
    "$N8N_PATH"
    "$ARTIFACTS_PATH"
)

for path in "${required_paths[@]}"; do
    if [ ! -d "$path" ]; then
        echo "Creating directory: $path"
        sudo mkdir -p "$path"
        sudo chown -R 1000:1000 "$path"
    fi
done

echo "All required paths validated and created if necessary."
