#!/bin/bash

# Source directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

echo "Stopping AutoDev Commander services..."
docker compose -f docker/compose/base.yml -f docker/compose/dev.yml down

echo "Services stopped"
