#!/bin/bash

# Validate paths first
./validate_paths.sh

# Start services
cd ..
docker compose -f docker/compose/base.yml -f docker/compose/dev.yml up -d

# Check service health
echo "Waiting for services to be healthy..."
sleep 10

docker compose ps
