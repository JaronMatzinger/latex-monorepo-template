#!/usr/bin/env bash
set -e

# Resolve current directory name dynamically
WORKSPACE_NAME="$(basename "$(pwd)")"

# Ensure output directory exists before compiling
mkdir -p report/PDF

CONTAINER_ID=$(docker ps -q --filter "label=devcontainer.local_folder=$(pwd)")

if [ -z "$CONTAINER_ID" ]; then
    echo "Error: Dev container is not running. Open VS Code or start it in OrbStack first."
    exit 1
fi

# Run inside the document directory so relative paths resolve cleanly
docker exec -w "/workspaces/${WORKSPACE_NAME}/report/document" "$CONTAINER_ID" \
    latexmk -pdf -interaction=nonstopmode -output-directory=../PDF main.tex
