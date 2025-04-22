#!/bin/bash

# Create main app structure
mkdir -p app/routes
mkdir -p app/templates
mkdir -p app/static/css
mkdir -p app/static/uploads
mkdir -p scripts

# Touch __init__.py files
touch app/__init__.py
touch app/routes/__init__.py

# Optionally make .env and README.md if not exist
if [ ! -f .env ]; then
  touch .env
  echo "# Add your secrets here" > .env
fi

if [ ! -f README.md ]; then
  touch README.md
  echo "# Dental AI Portal" > README.md
fi

echo "Project structure ready!"