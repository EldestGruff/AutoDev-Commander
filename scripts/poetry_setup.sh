#!/bin/bash

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Check Python version
echo "Python version:"
python3 --version

# Install Poetry if not exists
if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Update Poetry
poetry self update

# Clear any existing virtual environments
poetry env list
poetry env remove --all

# Create new virtual environment
poetry env use python3.11

# Install dependencies
poetry install

# Verify installation
poetry run python -c "import app; print('Import successful')"
